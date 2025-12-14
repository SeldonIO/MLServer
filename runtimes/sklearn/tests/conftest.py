import joblib
import pytest
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer

from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

from mlserver_sklearn import SKLearnModel
from mlserver_sklearn.sklearn import PREDICT_FN_KEY, PREDICT_TRANSFORM

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


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
        implementation=SKLearnModel,
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> SKLearnModel:
    model = SKLearnModel(model_settings)
    model.ready = await model.load()

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
        implementation=SKLearnModel,
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )

    model = SKLearnModel(settings)
    model.ready = await model.load()

    return model


@pytest.fixture
def pandas_model_uri(tmp_path) -> str:
    data: pd.DataFrame = pd.DataFrame(
        {"a": [1, 2, 3], "op": ["+", "+", "-"], "y": [11, 22, -33]}
    )

    X: pd.DataFrame = data.drop("y", axis=1)
    y: pd.DataFrame = data["y"]

    numeric_features = ["a"]
    numeric_transformer = StandardScaler()

    categorical_features = ["op"]
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[("preprocessor", preprocessor), ("regression", DummyRegressor())]
    )

    model.fit(X, y)

    model_uri = os.path.join(tmp_path, "sklearn-pandas-model.joblib")
    joblib.dump(model, model_uri)

    return model_uri


@pytest.fixture
def pandas_model_settings(pandas_model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="sklearn-pandas-model",
        implementation=SKLearnModel,
        parameters=ModelParameters(uri=pandas_model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def pandas_model(pandas_model_settings: ModelSettings) -> SKLearnModel:
    model = SKLearnModel(pandas_model_settings)
    model.ready = await model.load()

    return model


@pytest.fixture
def pandas_inference_request() -> InferenceRequest:
    inference_request = {
        "parameters": {"content_type": "pd"},
        "inputs": [
            {"name": "a", "datatype": "INT32", "data": [10], "shape": [1]},
            {
                "name": "op",
                "datatype": "BYTES",
                "data": ["-"],
                "shape": [1],
                "parameters": {"content_type": "str"},
            },
        ],
    }
    return InferenceRequest.model_validate(inference_request)


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


@pytest.fixture
async def dataframe_model(model_settings: ModelSettings) -> SKLearnModel:
    dummy = DummyDataframeModel()

    model = SKLearnModel(model_settings)
    model.ready = await model.load()

    # Replace internal model with dummy model
    model._model = dummy
    return model


@pytest.fixture
def pandas_preprocessor_uri(tmp_path) -> str:
    data: pd.DataFrame = pd.DataFrame(
        {"a": [1, 2, 3], "op": ["+", "+", "-"], "y": [11, 22, -33]}
    )

    X: pd.DataFrame = data.drop("y", axis=1)
    y: pd.DataFrame = data["y"]

    numeric_features = ["a"]
    numeric_transformer = StandardScaler()

    categorical_features = ["op"]
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    preprocessor.fit(X, y)

    model_uri = os.path.join(tmp_path, "sklearn-preprocessor-model.joblib")
    joblib.dump(preprocessor, model_uri)

    return model_uri


@pytest.fixture
def pandas_preprocessor_settings(pandas_preprocessor_uri: str) -> ModelSettings:
    return ModelSettings(
        name="sklearn-preprocessor-model",
        implementation=SKLearnModel,
        parameters=ModelParameters(
            uri=pandas_preprocessor_uri,
            version="v1.2.3",
            extra={PREDICT_FN_KEY: PREDICT_TRANSFORM},
        ),
    )


@pytest.fixture
async def pandas_preprocessor(
    pandas_preprocessor_settings: ModelSettings,
) -> SKLearnModel:
    model = SKLearnModel(pandas_preprocessor_settings)
    model.ready = await model.load()

    return model
