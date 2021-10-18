from data_prep import matches_to_table
import pandas as pd

if __name__ == "__main__":

    """
    Ideen Feature Engineering
    Einfache KPI, zB Durchschnittliche Tore via HappyLearning lernen lassen
    Durchschnittliche Punkte der letzen 3,4,5 Spiele -> "Lauf haben". Cold Start, aber o.k.. 
    Alternativ: Letzte Saison übernehmen
    """

    df_matches = pd.read_csv("data/results_19_20.csv")
    print(df_matches)
    table = matches_to_table(df_matches)
    print(table[table.matchday == 13])
