import pytest
import os
import asyncio
import numpy as np
import xgboost as xgb

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver.utils import install_uvloop_event_loop

from mlserver_xgboost import XGBoostModel
from mlserver_xgboost.xgboost import WELLKNOWN_MODEL_FILENAMES

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


@pytest.fixture
def event_loop():
    # By default use uvloop for tests
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(params=WELLKNOWN_MODEL_FILENAMES)
def model_uri(request, tmp_path) -> str:
    n = 4
    d = 3

    dtrain = xgb.DMatrix(data=np.random.rand(n, d), label=np.random.rand(n))
    bst = xgb.train(params={}, dtrain=dtrain)

    _, ext = os.path.splitext(request.param)
    model_uri = os.path.join(tmp_path, f"xgboost-model{ext}")
    bst.save_model(model_uri)

    return model_uri


@pytest.fixture
def classifier_uri(tmp_path) -> str:
    n = 5
    d = 3
    c = 5

    X_train = np.random.rand(n, d)
    y_train = [label for label in range(0, c)]
    clf = xgb.XGBClassifier(
        num_class=c, use_label_encoder=False, objective="multi:softprob"
    )
    clf.fit(X_train, y_train, eval_set=[(X_train, y_train)])

    model_uri = os.path.join(tmp_path, "xgboost-model.json")
    clf.save_model(model_uri)

    return model_uri


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="xgboost-model",
        implementation=XGBoostModel,
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> XGBoostModel:
    model = XGBoostModel(model_settings)
    model.ready = await model.load()

    return model


@pytest.fixture
async def classifier(classifier_uri: str) -> XGBoostModel:
    model_settings = ModelSettings(
        name="xgboost-model",
        implementation=XGBoostModel,
        parameters=ModelParameters(uri=classifier_uri, version="v1.2.3"),
    )
    model = XGBoostModel(model_settings)
    model.ready = await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
