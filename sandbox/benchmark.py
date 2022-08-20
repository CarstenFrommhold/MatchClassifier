import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score


def predict_result(odd_h, odd_d, odd_a):
    min_ = min(odd_h, odd_d, odd_a)
    if odd_h == min_:
        return "1"
    elif odd_d == min_:
        return "X"
    else:
        return "2"


def odds_to_array(odd_h, odd_d, odd_a):
    # Needs to fit the order specified in roc_auc_score
    return [odd_h, odd_a, odd_d]


def sum_(a, b, c):
    return a+b+c


if __name__ == "__main__":

    season = 2122

    df = pd.read_csv(f"../data/matches/s_{season}.csv")
    df = df.rename({
        "FTHG": "HomeGoals",
        "FTAG": "AwayGoals"
    }, axis="columns")

    # Prepare predict() output
    df['predicted_result'] = df.apply(
        lambda row: predict_result(row['B365H'], row['B365D'], row['B365A']), axis=1)

    # Prepare predict_proba() output
    for result in ["H", "D", "A"]:
        df[f"predicted_proba_{result}"] = 1 / df[f"B365{result}"]
    df["sum_of_probas"] = df.apply(
        lambda row: sum_(row['predicted_proba_H'], row['predicted_proba_D'], row['predicted_proba_A']), axis=1)
    for result in ["H", "D", "A"]:
        df[f"predicted_proba_{result}"] = df[f"predicted_proba_{result}"] / df["sum_of_probas"]

    df['odds_as_array'] = df.apply(
        lambda row: odds_to_array(row['predicted_proba_H'],
                                  row['predicted_proba_D'],
                                  row['predicted_proba_A']), axis=1
    )
    df["Goal_difference"] = df["HomeGoals"] - df["AwayGoals"]
    df["Points_Home"] = df["Goal_difference"].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)
    df["result"] = df["Points_Home"].replace({
        3: "1", 1: "X", 0: "2"
    })

    print(f"To get an idea of a benchmark. B365 odds given season {season} leads to:")
    print(f"Accuracy: {round(accuracy_score(df['predicted_result'], df['result']), 3)}")
    print(f"Precision: {round(precision_score(df['predicted_result'], df['result'], average='weighted'), 3)}")
    print(f"Recall: {round(recall_score(df['predicted_result'], df['result'], average='weighted'), 3)}")

    # Convert to np array with shape (306, ) resp. (306, 3) to use roc_auc_score
    results_np = df["result"].to_numpy()
    odds_np = np.asarray(df['odds_as_array'].to_list())

    roc = roc_auc_score(y_true=results_np,
                        y_score=odds_np,
                        labels=["1", "2", "X"],  # must be ordered
                        multi_class="ovr")  # ovo, ovr
    print(f"Auc: {round(roc, 3)}")
