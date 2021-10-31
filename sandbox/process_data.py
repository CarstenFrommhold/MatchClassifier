import match_classifier.data_prep as data_prep
import pandas as pd

write: bool = True

if __name__ == "__main__":

    # seasons = [1011, 1112, 1213, 1314, 1415, 1516, 1617, 1718, 1819, 2021]
    seasons = [1415, 1516, 1617, 1718, 1819, 2021]
    from_, to_ = 14, 21
    for season in seasons:
        print(f"Preparing data for season {season}")
        df_matches = pd.read_csv(f"../data/matches/s_{season}.csv")
        fifa_version = str(season)[2:]
        df_players = pd.read_csv(f"../data/players/players_{fifa_version}.csv")

        df_matches = data_prep.main(df_matches, df_players, season)
        if write:
            df_matches.to_csv(f"../data/prepared_matches/s_{season}.csv", index=False)

    df = pd.concat([pd.read_csv(f"../data/prepared_matches/s_{season}.csv") for season in seasons])
    if write:
        df.to_csv(f"../data/prepared_matches/training_data_{from_}_to_{to_}.csv", index=False)
    for col in df.columns:
        print(col)
