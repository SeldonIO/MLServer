import joblib
import pytest
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer

from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

from mlserver_sklearn import SKLearnModel

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
def model_uri(tmp_path) -> str:
    n = 4
    X = np.random.rand(n)
    y = np.random.rand(n)

    clf = DummyClassifier(strategy="prior")
    clf.fit(X, y)

    model_uri = os.path.join(tmp_path, "sklearn-model.joblib")
    joblib.dump(clf, model_uri)

    return model_uri


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="sklearn-model",
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> SKLearnModel:
    model = SKLearnModel(model_settings)
    await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)


@pytest.fixture
async def regression_model(tmp_path) -> SKLearnModel:
    # Build a quick DummyRegressor
    n = 4
    X = np.random.rand(n)
    y = np.random.rand(n)

    clf = DummyRegressor()
    clf.fit(X, y)

    model_uri = os.path.join(tmp_path, "sklearn-regression-model.joblib")
    joblib.dump(clf, model_uri)

    settings = ModelSettings(
        name="sklearn-regression-model",
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )

    model = SKLearnModel(settings)
    await model.load()

    return model


@pytest.fixture
def pandas_model_uri(tmp_path) -> str:
    data: pd.DataFrame = pd.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "op": ["+", "+", "-"], "y": [12, 15, -12]})

    X: pd.DataFrame = data.drop("y", axis=1)
    y: pd.DataFrame = data["y"]

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
        steps=[("preprocessor", preprocessor),
               ("regression", MLPRegressor(alpha=0.001, max_iter=2, hidden_layer_sizes=(4)))]
    )

    model.fit(X, y)

    model_uri = os.path.join(tmp_path, "sklearn-pandas-model.joblib")
    joblib.dump(model, model_uri)

    return model_uri


@pytest.fixture
def pandas_model_settings(pandas_model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="sklearn-pandas-model",
        parameters=ModelParameters(uri=pandas_model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def pandas_model(pandas_model_settings: ModelSettings) -> SKLearnModel:
    model = SKLearnModel(pandas_model_settings)
    await model.load()

    return model


@pytest.fixture
def pandas_inference_request() -> InferenceRequest:
    inference_request = {
        "parameters": {
            "content_type": "pd"
        },
        "inputs": [
            {
                "name": "a",
                "datatype": "INT32",
                "data": [10],
                "shape": [1]
            },
            {
                "name": "b",
                "datatype": "INT32",
                "data": [7],
                "shape": [1]
            },
            {
                "name": "c",
                "datatype": "INT32",
                "data": [6],
                "shape": [1]
            },
            {
                "name": "op",
                "datatype": "BYTES",
                "data": ["-"],
                "shape": [1],
                "parameters": {
                    "content_type": "str"
                }
            }
        ]
    }
    return InferenceRequest.parse_obj(inference_request)
