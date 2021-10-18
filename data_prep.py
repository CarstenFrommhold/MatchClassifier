import pandas as pd
import numpy as np
import pandasql as psql

"""
TODO: 
- Nachholspiele korrigieren auf ursprüngliches Datum
- Übersetzen in Datetime. Beachte Switch ab Saison 1819
- Dann sortieren nach Datum
- Nachholspiele korrigieren
- Stammdaten Vereine 
- Wo steckt Heimvorteil? 
"""


def main(df_matches: pd.DataFrame) -> pd.DataFrame:

    df_matches = prepare_matches(df_matches)
    df_matches = df_matches[["matchday", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"]]
    df_table = matches_to_table(df_matches)
    sanity_check_table(df_table)

    for kpi in ["Goals", "Goals_against", "Goal_difference", "Points"]:
        df_table[f"Avg_{kpi}"] = df_table[kpi] / df_table["matchday"]

    df_matches["matchday_pre"] = df_matches["matchday"] - 1

    q = """
    SELECT a.*,
           b.Position as HomePosition,
           b.Avg_Points as HomeAvgPoints,
           c.Position as AwayPosition,
           c.Avg_Points as AwayAvgPoints
    FROM df_matches a
    INNER JOIN df_table b
    INNER JOIN df_table c
    ON a.HomeTeam = b.Team AND a.matchday_pre = b.matchday 
    AND a.HomeTeam = c.Team AND a.matchday_pre = c.matchday
    """
    df_matches = psql.sqldf(q, locals())  # https://github.com/yhat/pandasql/issues/53

    return df_matches


def prepare_matches(df_matches: pd.DataFrame) -> pd.DataFrame:
    df_matches = df_matches.rename({
        "FTHG": "HomeGoals",
        "FTAG": "AwayGoals"
    }, axis="columns")
    df_matches["matchday"] = np.ceil((df_matches.index + 1) / 9)
    return df_matches


def matches_to_table(df_matches: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a table dataframe given a dataframe with matches
    Assumptions:
    - List of matches is sorted correctly (ascending with respect to matchdays)
    - Matches contains columns "matchday", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"
    """

    df_matches = prepare_matches(df_matches)
    df_matches["Goal_difference"] = df_matches["HomeGoals"] - df_matches["AwayGoals"]
    df_matches["Points_Home"] = df_matches["Goal_difference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)

    keep = ["matchday", "HomeTeam", "AwayTeam", "HomeGoals", "AwayGoals"]
    df_home = df_matches.loc[:, keep].rename(
        {"HomeTeam": "Team",
         "AwayTeam": "Opponent",
         "HomeGoals": "Goals",
         "AwayGoals": "Goals_against"}, axis="columns")
    df_home["Goal_difference"] = df_home["Goals"] - df_home["Goals_against"]
    df_home["Points"] = df_home["Goal_difference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)

    df_away = df_matches.loc[:, keep].rename(
        {"AwayTeam": "Team",
         "HomeTeam": "Opponent",
         "AwayGoals": "Goals",
         "HomeGoals": "Goals_against"}, axis="columns")
    df_away["Goal_difference"] = df_away["Goals"] - df_away["Goals_against"]
    df_away["Points"] = df_away["Goal_difference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)

    df = pd.concat([df_home, df_away], axis=0)
    df = df.sort_values(by=["Team", "matchday"])
    df = df.groupby(['Team', 'matchday']).sum().groupby(level=0).cumsum().reset_index()
    df = df.sort_values(by=["matchday", "Points", "Goal_difference"], ascending=False)
    df["Position"] = df.groupby(["matchday"]).cumcount() + 1

    df = add_matchday_zero(df)

    if not sanity_check_table(df):
        raise SanityError("Take a look at the table creation.")

    return df


def add_matchday_zero(table: pd.DataFrame) -> pd.DataFrame:

    teams = table["Team"].unique()
    cols_without_team = [col for col in table.columns.to_list() if col != "Team"]
    md_0 = pd.DataFrame(
        [[team] + [0] * len(cols_without_team) for team in teams],
        columns=["Team"] + cols_without_team)
    return pd.concat([md_0, table]).reset_index().drop(columns=["index"])


def sanity_check_table(df_table: pd.DataFrame) -> bool:
    """Each matchday should include 18 teams."""
    return df_table.groupby(by=["matchday"]).Team.count().unique() == [18]


class SanityError(Exception):
    """ Raises if Sanity Check fails."""
    pass

