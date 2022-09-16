import pandas as pd
import pendulum
import os
import sys
import match_classifier.data_prep as data_prep
from typing import Dict, Tuple
import joblib
from match_classifier.utils import map_names
from match_classifier.config import FEATURES

current_season: str = "2223"
matchplan_path = f"../../data/current_season/matchplan_{current_season}.csv"


def update_current_season():

    matches = f'https://www.football-data.co.uk/mmz4281/{current_season}/D1.csv'

    if sys.platform == "darwin":  # macos
        os.system(f"curl -o ../../data/current_season/s_{current_season}.csv {matches}")
    else:
        os.system(f"echo download {matches}")
        os.system(f"wget {matches} ")
        os.system(f"mv D1.csv ../../data/current_season/s_{current_season}.csv")


def rename(df):

    df = df.rename({
        "Spieltag": "Matchday",
        "Heimmannschaft": "HomeTeam",
        "Gastmannschaft": "AwayTeam"
    }, axis=1)

    return df


def reciprocal_value(x: float) -> float:
    if x == 0:
        return 99
    else:
        return 1/x


def create_twitter_messages(df_predictions: pd.DataFrame, matchday: int) -> Tuple[str, str]:

    abbreviations: Dict = {
        "Freiburg": "FRE",
        "Werder Bremen": "SVW",
        "Hoffenheim": "HOF",
        "Hertha": "BSC",
        "M'gladbach": "BMG",
        "Bochum": "VFL",
        "Augsburg": "AUG",
        "Stuttgart": "STU",
        "Leverkusen": "LEV",
        "Wolfsburg": "WOB",
        "Ein Frankfurt": "FRA",
        "RB Leipzig": "RBL",
        "Dortmund": "BVB",
        "FC Koln": "FCK",
        "Union Berlin": "FCU",
        "Bayern Munich": "BAY",
        "Schalke 04": "S04",
        "Mainz": "MAI"
    }

    df_predictions = df_predictions.replace(abbreviations)
    message_1 = f"(1/2) Odds for next weekend, matchday {matchday}."
    message_2 = f"(2/2) Odds for next weekend, matchday {matchday}."

    for match in df_predictions.iterrows():
        match_no, entries = match
        str_ = entries["HomeTeam"] + "-" + entries["AwayTeam"] + " " + str(entries["1"]) + " | " \
        + str(entries["X"]) + " | " + str(entries["2"])
        if match_no <= 4:
            message_1 = message_1 + "\r\n" + str_
        else:
            message_2 = message_2 + "\r\n" + str_

    return message_1, message_2


if __name__ == "__main__":

    update_current_season()
    df_matchplan = pd.read_csv(matchplan_path)
    df_matchplan = rename(df_matchplan)

    df_matches_played = pd.read_csv("../../data/current_season/s_2223.csv")
    df_players = pd.read_csv("../../data/players/players_22.csv")

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
    data = data_prep.main(data, df_players, season=2122, full_season=False)

    keep = ["Matchday", "HomeTeam", "AwayTeam"] + FEATURES
    df_prediction_input = data.loc[data.Matchday == next_matchday, keep].reset_index().drop("index", axis=1)
    model = joblib.load("../model/model.p")
    df_prediction_input[FEATURES].to_csv("cftest.csv")
    predictions = model.predict_proba(df_prediction_input[FEATURES])
    df_odds = pd.DataFrame(predictions, columns=["1", "2", "X"])
    for result in ["1", "2", "X"]:
        df_odds[result] = df_odds[result].apply(lambda x: round(reciprocal_value(x), 2))
        df_odds[result] = df_odds[result].apply(lambda x: min(x, 20))
    df_predictions = df_prediction_input[["HomeTeam", "AwayTeam"]].join(df_odds)
    message_1, message_2 = create_twitter_messages(df_predictions, int(next_matchday))
    print(message_1)
    print(message_2)
    with open("twitter_message_1.txt", "w") as file:
        file.write(message_1)
    with open("twitter_message_2.txt", "w") as file:
        file.write(message_2)
