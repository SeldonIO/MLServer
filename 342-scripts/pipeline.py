import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

import pandas as pd

np.random.seed(0)
data = pd.read_csv("342-scripts/data.csv")
X = data.drop("y", axis=1)
y = data["y"]

numeric_features = ["a", "b", "c"]
# Doesn't really do anything, just messing around with transformers
numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
)

categorical_features = ["op"]
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

model = Pipeline(
    steps=[("preprocessor", preprocessor), ("regression", MLPRegressor(alpha=0.001, max_iter=10000, hidden_layer_sizes=(5)))]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model.fit(X_train, y_train)

print("model score: %.3f" % model.score(X_test, y_test))

# Save it
import pickle
with open("342-scripts/model.pkl", "wb") as f:
    pickle.dump(model, f)
