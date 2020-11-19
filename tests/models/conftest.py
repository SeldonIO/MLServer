import pytest
import os

from mlserver.models.sklearn import _SKLEARN_PRESENT, SKLearnModel
from mlserver.models.xgboost import _XGBOOST_PRESENT, XGBoostModel
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest, TensorData

if _SKLEARN_PRESENT:
    import joblib

    from sklearn.dummy import DummyClassifier

if _XGBOOST_PRESENT:
    import xgboost as xgb

if _SKLEARN_PRESENT or _XGBOOST_PRESENT:
    import numpy as np


@pytest.fixture
def sklearn_model_uri(tmp_path) -> str:
    n = 4
    X = np.random.rand(n)
    y = np.random.rand(n)

    clf = DummyClassifier(strategy="prior")
    clf.fit(X, y)

    model_uri = os.path.join(tmp_path, "sklearn-model.joblib")
    joblib.dump(clf, model_uri)

    return model_uri


@pytest.fixture
def sklearn_model_settings(sklearn_model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="sklearn-model",
        parameters=ModelParameters(uri=sklearn_model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def sklearn_model(sklearn_model_settings: ModelSettings) -> SKLearnModel:
    model = SKLearnModel(sklearn_model_settings)
    await model.load()

    return model


@pytest.fixture
def sklearn_inference_request(inference_request: InferenceRequest) -> InferenceRequest:
    # Keep only a single input
    inference_request.inputs = inference_request.inputs[:1]

    return inference_request


@pytest.fixture
def xgboost_model_uri(tmp_path) -> str:
    n = 4
    d = 3

    dtrain = xgb.DMatrix(data=np.random.rand(n, d), label=np.random.rand(n))
    bst = xgb.train(params={}, dtrain=dtrain)

    model_uri = os.path.join(tmp_path, "xgboost-model.json")
    bst.save_model(model_uri)

    return model_uri


@pytest.fixture
def xgboost_model_settings(xgboost_model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="xgboost-model",
        parameters=ModelParameters(uri=xgboost_model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def xgboost_model(xgboost_model_settings: ModelSettings) -> XGBoostModel:
    model = XGBoostModel(xgboost_model_settings)
    await model.load()

    return model


@pytest.fixture
def xgboost_inference_request(inference_request: InferenceRequest) -> InferenceRequest:
    # Reshape to 2D array, matching the input data to xgboost_model
    single_input = inference_request.inputs[0]
    single_input.data = TensorData.parse_obj([[1, 2, 3]])
    single_input.shape = [1, 3]

    # Keep only a single input
    inference_request.inputs = [single_input]

    return inference_request
