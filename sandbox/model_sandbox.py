import pandas as pd
from match_classifier.model.baseline import DecisionTreeModel, Random, Simple
from match_classifier.config import FEATURES
import joblib


if __name__ == "__main__":

    data = pd.read_csv("../data/prepared_matches/training_data_14_to_21.csv")
    data = data.loc[data.Matchday >= 6]
    target = "result"

    model = DecisionTreeModel(
        data, FEATURES, target, max_depth=3, min_samples_leaf=0.03)
    #model = Random(data, FEATURES, target)
    #model = Simple(data, FEATURES, target)
    model.load_data()
    model.train()
    model.evaluate()
    print(model.accuracy, model.precision, model.auc)

    model.final_fit()
    joblib.dump(model.tree, "model/model.p")

