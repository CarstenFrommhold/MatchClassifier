""" Baseline classes
"""
import pandas as pd
import random as rd


class Baseline:

    def __init__(self):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass


class Random(Baseline):

    def predict(self, X: pd.DataFrame):
        return pd.Series([rd.choice(["1", "x", "2"]) for _ in range(len(X))])


class Simple(Baseline):

    def fit(self, X, y):
        distribution = y.value_counts(normalize=True)
        self.argmax = distribution.idxmax()
        print(f"Learned: {distribution}")

    def predict(self, X):
        return pd.Series([self.argmax for _ in range(len(X))])


"""
Some other ideas:
- Predict given the results of the last games between two teams
- Predict given the results of the last teams (row)
- Predict given simple classifications
"""
