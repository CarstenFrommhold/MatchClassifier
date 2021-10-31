import pandas as pd
from match_classifier.data_prep import top_n_player_skills


if __name__ == "__main__":

    season = 2122
    fifa_version = str(season)[2:]
    df = pd.read_csv(f"../data/players/players_{fifa_version}.csv")
    df_avg = top_n_player_skills(df, season)
    print(df_avg)
