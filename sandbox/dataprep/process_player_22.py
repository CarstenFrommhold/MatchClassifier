import pandas as pd

if __name__ == "__main__":

    # process 22 https://www.kaggle.com/cashncarry/fifa-22-complete-player-dataset
    df = pd.read_csv(f"../../data/players/players_fifa22.csv")
    df = df.rename({"FullName": "long_name",
                    "Club": "club_name",
                    "Overall": "overall"}, axis=1)
    buli_clubs_in_22 = [
        "FC Bayern München",
        "Borussia Dortmund",
        "RB Leipzig",
        "Borussia Mönchengladbach",
        "VfL Wolfsburg",
        "Eintracht Frankfurt",
        "1. FC Union Berlin",
        "Hertha BSC",
        "Sport-Club Freiburg",
        "VfL Bochum 1848",
        "SpVgg Greuther Fürth",
        "FC Augsburg",
        "1. FSV Mainz 05",
        "Bayer 04 Leverkusen",
        "1. FC Köln",
        "DSC Arminia Bielefeld",
        "VfB Stuttgart",
        "TSG Hoffenheim"
    ]
    def help_name(x):
        if x in buli_clubs_in_22:
            return 'German 1. Bundesliga'
        else:
            return "sonst"
    df["league_name"] = df["club_name"].apply(lambda x: help_name(x))
    print(df)
    df.to_csv("../../data/players/players_22.csv")


