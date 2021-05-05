import os
import mlflow
import pytest
import numpy as np

from sklearn.dummy import DummyClassifier
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

from mlserver_mlflow import MLflowRuntime

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

    model_path = os.path.join(tmp_path, "dummy-model")
    mlflow.sklearn.save_model(clf, path=model_path)

    return model_path


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="mlflow-model",
        parameters=ModelParameters(uri=model_uri),
    )


@pytest.fixture
async def runtime(model_settings: ModelSettings) -> MLflowRuntime:
    model = MLflowRuntime(model_settings)
    await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
