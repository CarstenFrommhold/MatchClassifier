import fuzzywuzzy.fuzz
import pandas as pd
import numpy as np
import os
import sys
sys.path.append("../training/data_prep")
import data_prep
from typing import List, Dict


matchplan_path = "data/matchplan_2122.csv"


def download_status_quo():

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

    # download_status_quo()

    matchplan = pd.read_csv(matchplan_path)
    matchplan = rename(matchplan)
    matches_so_far = pd.read_csv("data/s_2122.csv")
    matches_so_far = data_prep.main(matches_so_far, full_season=False)
    print(matches_so_far)
    print(matchplan)

