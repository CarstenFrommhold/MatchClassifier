""" Baseline classes
"""
import pandas as pd
import random as rd
from typing import List
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score


class Baseline:

    def __init__(self, data: pd.DataFrame, features: List[str], target: str):
        self.data = data
        self.features = features
        self.target = target

    def load_data(self):
        x, y = self.data[self.features], self.data[self.target]
        self.x_train, self.x_test, self.y_train, self.y_test = \
            train_test_split(x, y, test_size=0.33, random_state=42)

    def evaluate(self):
        self.y_pred = self.predict(self.x_test)
        self.precision = precision_score(self.y_test, self.y_pred, average="weighted")
        self.recall = recall_score(self.y_test, self.y_pred, average="weighted")
        self.accuracy = accuracy_score(self.y_test, self.y_pred)
        try:
            self.y_pred_proba = self.predict_proba(self.x_test)
            self.auc = roc_auc_score(self.y_test, self.y_pred_proba, multi_class="ovo")
        except:
           self.auc = "na"

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

    def predict_proba(self, X):
        pass

    def train(self):
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

    def train(self):
        self.fit(self.x_train, self.y_train)


class DecisionTreeModel(Baseline):

    def __init__(self, *args, max_depth: int, min_samples_leaf: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.tree = DecisionTreeClassifier(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)

    def fit(self, X, y):
        self.tree.fit(self.x_train, self.y_train)

    def final_fit(self):
        self.tree.fit(self.data[self.features], self.data[self.target])

    def predict(self, X):
        return self.tree.predict(X)

    def predict_proba(self, X):
        return self.tree.predict_proba(X)

    def train(self):
        self.fit(..., ...)
