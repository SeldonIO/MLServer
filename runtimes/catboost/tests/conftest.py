import pytest
import os
import numpy as np
from catboost import CatBoostClassifier  # , CatBoostRegressor, CatBoostRanker

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

from mlserver_catboost import CatboostModel

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


@pytest.fixture
def model_uri(tmp_path) -> str:
    train_data = np.random.randint(0, 100, size=(100, 10))
    train_labels = np.random.randint(0, 2, size=(100))

    model = CatBoostClassifier(
        iterations=2, depth=2, learning_rate=1, loss_function="Logloss", verbose=True
    )
    # TODO: add a selector for the regressor/ranker classes
    # model = CatBoostRegressor(
    #     iterations=2, depth=2, learning_rate=1, loss_function="RMSE", verbose=True
    # )
    # model = CatBoostRanker(
    #     iterations=2, depth=2, learning_rate=1, loss_function="RMSE", verbose=True
    # )
    model.fit(train_data, train_labels)

    model_uri = os.path.join(tmp_path, "model.cbm")
    model.save_model(model_uri)

    return model_uri


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="catboost-model",
        implementation=CatboostModel,
        parameters=ModelParameters(uri=model_uri, version="v1.2.3"),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> CatboostModel:
    model = CatboostModel(model_settings)
    await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
