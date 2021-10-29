import pandas as pd
from baseline import DecisionTreeModel, Random, Simple
import joblib

if __name__ == "__main__":

    data = pd.read_csv("../data/prepared_matches/training_data_10y.csv")
    data = data.loc[data.Matchday >= 6]
    features = ["HomeAvgPoints", "AwayAvgPoints", "AvgPointDelta",
                "HomePoints_last3", "HomeGoals_last3", "AwayPoints_last3", "AwayGoals_last3",
                "HomePoints_last5", "HomeGoals_last5", "AwayPoints_last5", "AwayGoals_last5"]
    target = "result"

    model = DecisionTreeModel(
        data, features, target, max_depth=3)
    #model = Random(data, features, target)
    #model = Simple(data, features, target)
    model.load_data()
    model.train()
    model.evaluate()
    print(model.accuracy, model.precision, model.auc)
    joblib.dump(model.tree, "model.p")

