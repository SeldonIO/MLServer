import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator


class DummyDataframeModel(BaseEstimator):
    """predict/_proba return data frames"""

    def predict(self, X):
        frame = pd.DataFrame()
        frame["label_1"] = np.array([1])
        frame["label_2"] = np.array([2])
        frame["label_3"] = 3
        return frame

    def predict_proba(self, X):
        frame = pd.DataFrame()
        frame["label_1_prob"] = np.array([0.123])
        frame["label_2_prob"] = np.array([0.456])
        frame["label_3_prob"] = 0.789
        return frame
