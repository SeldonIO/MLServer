import joblib
import pytest
import os
import numpy as np

from sklearn.dummy import DummyClassifier
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
