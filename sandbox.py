import data_prep
import pandas as pd


if __name__ == "__main__":

    """
    Ideen Feature Engineering
    Einfache KPI, zB Durchschnittliche Tore via HappyLearning lernen lassen
    Durchschnittliche Punkte der letzen 3,4,5 Spiele -> "Lauf haben". Cold Start, aber o.k.. 
    Alternativ: Letzte Saison übernehmen
    """

    seasons = [1011, 1112, 1213, 1314, 1415, 1516, 1617, 1718, 1819, 2021]
    for season in seasons:
        print(f"Preparing data for season {season}")
        df_matches = pd.read_csv(f"data/s_{season}.csv")
        df_matches = data_prep.main(df_matches)
        print(df_matches)
        print(df_matches.columns)
