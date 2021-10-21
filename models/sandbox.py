import pandas as pd
from baseline import DecisionTreeModel, Random, Simple

if __name__ == "__main__":

    data = pd.read_csv("../data/prepared_matches/10y.csv")
    data = data.loc[data.matchday >= 6]
    features = ["HomeAvgPoints", "AwayAvgPoints", "AvgPointDelta"]
    target = "result"

    model = DecisionTreeModel(
        data, features, target, max_depth=2)
    # model = Random(data, features, target)
    # model = Simple(data, features, target)
    model.load_data()
    model.train()
    model.evaluate()
    print(model.accuracy, model.precision, model.recall)

# For the moment, the performance sucks of course.
# But this should act as a template.
