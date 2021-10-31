""" Data preparation given -one- season
"""
import pandas as pd
import numpy as np
import pandasql as psql
import pendulum
from match_classifier.utils import map_names


def main(
    df_matches: pd.DataFrame, df_players: pd.DataFrame, season: int,
    full_season: bool = True, table_output_path: str = None
) -> pd.DataFrame:

    df_matches = prepare_matches(df_matches, full_season)
    df_matches = df_matches[["Matchday", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"]]
    df_table = matches_to_table(df_matches, full_season, table_output_path)

    for kpi in ["Goals", "GoalsAgainst", "GoalDifference", "Points"]:
        df_table[f"Avg_{kpi}"] = df_table[kpi] / df_table["Matchday"]

    df_matches["Matchday_pre"] = df_matches["Matchday"] - 1

    """ Some feature engineering 
    """

    q = """
    SELECT a.*,
           b.Position as HomePosition,
           b.Avg_Points as HomeAvgPoints,
           c.Position as AwayPosition,
           c.Avg_Points as AwayAvgPoints
    FROM df_matches a
    INNER JOIN df_table b
    INNER JOIN df_table c
    ON a.HomeTeam = b.Team AND a.Matchday_pre = b.Matchday 
    AND a.HomeTeam = c.Team AND a.Matchday_pre = c.Matchday
    """
    df_matches = psql.sqldf(q, locals())  # https://github.com/yhat/pandasql/issues/53
    df_matches = df_matches.drop("Matchday_pre", axis=1)

    df_matches["AvgPointDelta"] = df_matches["HomeAvgPoints"] - df_matches["AwayAvgPoints"]

    """ Add Player Skills
    """
    df_matches = add_player_skills(df_matches, df_players, season)

    """ Create target variable
    """
    df_matches = create_target_variable(df_matches)
    df_matches = add_rolling_kpi(df_matches)

    if full_season:
        if not sanity_check_matches(df_matches):
            raise SanityError("Take a look at the matches input.")

    df_matches["Season"] = season

    return df_matches


def add_player_skills(df_matches: pd.DataFrame, df_players: pd.DataFrame, season) -> pd.DataFrame:

    df_players = top_n_player_skills(df_players, season=season)
    map_dict = map_names(df_players.club_name.unique(), df_matches.HomeTeam.unique())
    df_players["club_name"] = df_players["club_name"].replace(map_dict)

    q = """
    SELECT a.*,
           b.mean_skill as HomeSkills,
           c.mean_skill as AwaySkills
    FROM df_matches a
    INNER JOIN df_players b
    INNER JOIN df_players c
    ON a.HomeTeam = b.club_name
    AND a.AwayTeam = c.club_name
    """
    df_matches = psql.sqldf(q, locals())
    print(df_matches["HomeSkills"])
    df_matches["SkillDelta"] = df_matches["HomeSkills"] - df_matches["AwaySkills"]

    return df_matches


def add_rolling_kpi(df_matches: pd.DataFrame) -> pd.DataFrame:
    """
    """
    df = df_matches.copy()

    df_home = df.rename({"HomeTeam": "Team", "HomePoints": "Points",
                         "HomeGoals": "Goals", "AwayGoals": "GoalsAgainst"}, axis=1)
    df_away = df.rename({"AwayTeam": "Team", "AwayPoints": "Points",
                         "AwayGoals": "Goals", "HomeGoals": "GoalsAgainst"}, axis=1)
    df_performance = pd.concat([df_home, df_away]).reset_index().drop("index", axis=1)
    df_performance = df_performance[["Matchday", "Team", "Points", "Goals", "GoalsAgainst"]]

    df_ = pd.DataFrame()
    for team in df_performance["Team"].unique():
        df_team_performance = df_performance[df_performance["Team"] == team].copy()
        df_team_performance = df_team_performance.sort_values(by=["Matchday", "Team"])

        for series in [3, 5]:
            df_team_performance[f"Points_last{series}"] = df_team_performance["Points"].rolling(series + 1).sum() - df_performance["Points"]
            df_team_performance[f"Goals_last{series}"] = df_team_performance["Goals"].rolling(series + 1).sum() - df_performance["Goals"]
            df_team_performance[f"GoalsAgainst_last{series}"] = df_team_performance["GoalsAgainst"].rolling(series + 1).sum() - df_performance["GoalsAgainst"]

        keep_ = ["Matchday", "Team"] + [col for col in df_team_performance.columns if "_last" in col]
        df_team_performance = df_team_performance[keep_]
        df_ = pd.concat([df_, df_team_performance])

    df_performance_home_prefix = df_.rename({col: f"Home{col}" for col in df_.columns if col != "Matchday"}, axis=1)
    df_performance_away_prefix = df_.rename({col: f"Away{col}" for col in df_.columns if col != "Matchday"}, axis=1)

    df_matches = df_matches.merge(df_performance_home_prefix, on=["Matchday", "HomeTeam"], how="left")
    df_matches = df_matches.merge(df_performance_away_prefix, on=["Matchday", "AwayTeam"], how="left")

    return df_matches


def create_target_variable(df_matches: pd.DataFrame) -> pd.DataFrame:

    df_matches["GoalDifference"] = df_matches["HomeGoals"] - df_matches["AwayGoals"]
    df_matches["HomePoints"] = df_matches["GoalDifference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)
    df_matches["AwayPoints"] = df_matches["GoalDifference"].apply(lambda x: 3 if x < 0 else 1 if x == 0 else 0)
    df_matches["result"] = df_matches["HomePoints"].replace({
        3: "1", 1: "X", 0: "2"
    })

    return df_matches


def prepare_matches(df_matches: pd.DataFrame, full_season: bool = True) -> pd.DataFrame:
    """
    - Rename Goal columns
    - Create Matchday column
        - correct catch up games
        - sort and create Matchday
    """
    df_matches = df_matches.rename({
        "FTHG": "HomeGoals",
        "FTAG": "AwayGoals"
    }, axis="columns")
    df_matches = correct_catch_up_matches(df_matches)
    df_matches = make_datetime(df_matches)
    df_matches = df_matches.sort_values(by="Datetime").reset_index().drop("index", axis=1)  # reset index!
    df_matches["Matchday"] = np.ceil((df_matches.index + 1) / 9)

    if full_season:
        if not sanity_check_matches(df_matches):
            raise SanityError("Take a look at the matches input.")

    return df_matches


def make_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """ One observes a switch in datetime format given the matches. """
    try:
        df["Datetime"] = df["Date"].apply(lambda x: pendulum.from_format(x, 'DD/MM/YY'))
    except:
        df["Datetime"] = df["Date"].apply(lambda x: pendulum.from_format(x, 'DD/MM/YYYY'))
    return df


def correct_catch_up_matches(df_matches: pd.DataFrame) -> pd.DataFrame:
    """
    Set originally planned date for all catch up matches
    Note the bias regarding the "current" table position
    """

    CATCH_UP_GAMES = {
        "29/01/14": "21/12/13",  # Stuttgart vs. Bayern
        "13/12/11": "19/11/11",  # Köln vs. Mainz
        "16/02/11": "05/02/11",  # HSV vs. St Pauli
        "10/03/2021": "06/02/2021",  # Bielefeld vs. Bremen
        "03/05/2021": "17/04/2021",  # Mainz vs. Hertha
        "06/05/2021": "20/04/2021",  # Hertha vs. Freiburg
        "12/05/2021": "24/04/2021",  # Schalke vs. Hertha
    }

    df_matches["Date"] = df_matches["Date"].replace(CATCH_UP_GAMES)

    return df_matches


def matches_to_table(
        df_matches: pd.DataFrame, full_season: bool = True,
        output_path: str = None) -> pd.DataFrame:
    """
    Creates a table dataframe given a dataframe with matches
    Assumptions:
    - List of matches is sorted correctly (ascending with respect to Matchdays)
    - Matches contains columns "Matchday", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"
    """

    keep = ["Matchday", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"]
    df_home = df_matches.loc[:, keep].rename(
        {"HomeTeam": "Team",
         "AwayTeam": "Opponent",
         "HomeGoals": "Goals",
         "AwayGoals": "GoalsAgainst"}, axis="columns")
    df_home["GoalDifference"] = df_home["Goals"] - df_home["GoalsAgainst"]
    df_home["Points"] = df_home["GoalDifference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)

    df_away = df_matches.loc[:, keep].rename(
        {"AwayTeam": "Team",
         "HomeTeam": "Opponent",
         "AwayGoals": "Goals",
         "HomeGoals": "GoalsAgainst"}, axis="columns")
    df_away["GoalDifference"] = df_away["Goals"] - df_away["GoalsAgainst"]
    df_away["Points"] = df_away["GoalDifference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)

    df = pd.concat([df_home, df_away], axis=0)
    df = df.sort_values(by=["Team", "Matchday"])
    df = df.groupby(['Team', 'Matchday']).sum().groupby(level=0).cumsum().reset_index()
    df = df.sort_values(by=["Matchday", "Points", "GoalDifference"], ascending=False)
    df["Position"] = df.groupby(["Matchday"]).cumcount() + 1

    df = add_matchday_zero(df)

    if full_season:
        if not sanity_check_table(df):
            raise SanityError("Take a look at the table creation.")

    if output_path:
        df.to_csv(output_path)

    return df


def add_matchday_zero(table: pd.DataFrame) -> pd.DataFrame:

    teams = table["Team"].unique()
    cols_without_team = [col for col in table.columns.to_list() if col != "Team"]
    md_0 = pd.DataFrame(
        [[team] + [0] * len(cols_without_team) for team in teams],
        columns=["Team"] + cols_without_team)
    return pd.concat([table, md_0]).reset_index().drop(columns=["index"])


def sanity_check_table(df_table: pd.DataFrame) -> bool:
    """Each Matchday should include 18 teams."""
    return list(df_table.groupby(by=["Matchday"]).Team.count().unique()) == [18]


def sanity_check_matches(df_matches: pd.DataFrame) -> bool:
    """ 306 matches and 17 matches for each Home & Away Team. """
    s1 = len(df_matches) == 306
    s2 = list(df_matches.groupby(by=["HomeTeam"]).AwayTeam.count().unique()) == [17]
    s3 = list(df_matches.groupby(by=["AwayTeam"]).HomeTeam.count().unique()) == [17]
    s4 = list(df_matches.groupby(by=["Matchday"]).HomeTeam.count().unique()) == [9]
    return s1 and s2 and s3 and s4


class SanityError(Exception):
    """ Raises if Sanity Check fails."""
    pass


def top_n_player_skills(df: pd.DataFrame, season: int, league_name: str = 'German 1. Bundesliga', top_n: int = 15) -> pd.DataFrame:

    df = df.loc[df.league_name == league_name,
                ["long_name", "club_name", "overall"]]
    df = df.sort_values(by=["club_name", "overall"], ascending=False).reset_index().drop("index", axis=1)
    df = df.groupby('club_name').head(top_n).reset_index(drop=True)
    df_avg = df.groupby(by="club_name").mean().reset_index().rename({"overall": "mean_skill"}, axis=1).sort_values(by="mean_skill", ascending=False)
    df_avg["season"] = season

    return df_avg
