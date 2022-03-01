import pytest
import os
import numpy as np
import xgboost as xgb

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

from mlserver_xgboost import XGBoostModel

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


@pytest.fixture
def model_uri(tmp_path) -> str:
    n = 4
    d = 3

    dtrain = xgb.DMatrix(data=np.random.rand(n, d), label=np.random.rand(n))
    bst = xgb.train(params={}, dtrain=dtrain)

    model_uri = os.path.join(tmp_path, "xgboost-model.json")
    bst.save_model(model_uri)

    return model_uri


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="xgboost-model",
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> XGBoostModel:
    model = XGBoostModel(model_settings)
    await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
