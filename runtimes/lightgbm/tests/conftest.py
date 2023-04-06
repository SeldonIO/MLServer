import pytest
import os
import asyncio
import numpy as np
import lightgbm as lgb

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver.utils import install_uvloop_event_loop

from mlserver_lightgbm import LightGBMModel

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


@pytest.fixture
def event_loop():
    # By default use uvloop for tests
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def model_uri(tmp_path) -> str:
    n = 4
    d = 3

    train = lgb.Dataset(data=np.random.rand(n, d), label=np.random.rand(n))
    print(train)
    bst = lgb.train(params={}, train_set=train)

    model_uri = os.path.join(tmp_path, "lightgbm-model.bst")
    bst.save_model(model_uri)

    return model_uri


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="lightgbm-model",
        implementation=LightGBMModel,
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> LightGBMModel:
    model = LightGBMModel(model_settings)
    model.ready = await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
