import data_prep
import pandas as pd


if __name__ == "__main__":

    """
    Ideen Feature Engineering
    Einfache KPI, zB Durchschnittliche Tore via HappyLearning lernen lassen
    Durchschnittliche Punkte der letzen 3,4,5 Spiele -> "Lauf haben". Cold Start, aber o.k.. 
    Alternativ: Letzte Saison übernehmen
    """

    df_matches = pd.read_csv("data/s_1819.csv")
    df_matches = data_prep.main(df_matches)
    print(df_matches)
