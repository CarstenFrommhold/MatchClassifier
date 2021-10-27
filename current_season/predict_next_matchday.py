import fuzzywuzzy.fuzz
import pandas as pd
import numpy as np
import pendulum
import os
import sys
sys.path.append("../training/data_prep")
import data_prep
from typing import List, Dict


matchplan_path = "data/matchplan_2122.csv"
features = ["HomeAvgPoints", "AwayAvgPoints", "AvgPointDelta",
            "HomePoints_last3", "HomeGoals_last3", "AwayPoints_last3", "AwayGoals_last3",
            "HomePoints_last5", "HomeGoals_last5", "AwayPoints_last5", "AwayGoals_last5"]


def update_current_season():

    matches = f'https://www.football-data.co.uk/mmz4281/2122/D1.csv'
    os.system(f"echo download {matches}")
    os.system(f"wget {matches} ")
    os.system(f"mv D1.csv data/s_2122.csv")


def rename(df):

    df = df.rename({
        "Spieltag": "Matchday",
        "Heimmannschaft": "HomeTeam",
        "Gastmannschaft": "AwayTeam"
    }, axis=1)

    return df


def map_names(from_: List[str], to: List[str]) -> Dict:
    """ Simple mapping helper
    Allocate each entry in from_ to the "nearest" entry in to
    """
    map = {}
    for entry_from in from_:
        ratios = [fuzzywuzzy.fuzz.ratio(entry_from, entry_to) for entry_to in to]
        map[entry_from] = to[np.argmax(ratios)]
    return map


if __name__ == "__main__":

    # update_current_season()
    df_matchplan = pd.read_csv(matchplan_path)
    df_matchplan = rename(df_matchplan)

    df_matches_played = pd.read_csv("data/s_2122.csv")

    n_matches_played = len(df_matches_played)
    if n_matches_played % 9 != 0:
        raise Exception("Missing matches in current status.")
    next_matchday = n_matches_played/9 + 1
    df_next_matchday: pd.DataFrame = df_matchplan[df_matchplan["Matchday"] == next_matchday]

    team_names_from = df_matchplan["HomeTeam"].unique()
    team_names_to = df_matches_played["HomeTeam"].unique()
    map_names = map_names(team_names_from, team_names_to)
    df_next_matchday = df_next_matchday.replace(map_names)[["Matchday", "HomeTeam", "AwayTeam"]]
    df_next_matchday["Date"] = pendulum.today().format("DD/MM/YYYY")
    df_next_matchday["FTAG"] = 9999
    df_next_matchday["FTHG"] = 9999

    data = pd.concat([df_matches_played, df_next_matchday]).reset_index().drop("index", axis=1)
    data = data_prep.main(data, full_season=False, table_output_path="sanity_table.csv")

    keep = ["Matchday", "HomeTeam", "AwayTeam"] + features
    df_prediction_input = data.loc[data.Matchday == next_matchday, keep]
    print(df_prediction_input)

