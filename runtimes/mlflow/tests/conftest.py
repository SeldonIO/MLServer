import os
import sys
import mlflow
import pytest
import numpy as np

from sklearn.dummy import DummyClassifier
from mlflow.models.signature import ModelSignature, infer_signature
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
def dataset() -> tuple:
    n = 4
    X = np.random.rand(n)
    y = np.random.rand(n)

    return X, y


@pytest.fixture
def model_signature(dataset: tuple) -> ModelSignature:
    X, y = dataset
    signature = infer_signature(X, y)

    signature.inputs.inputs[0]._name = "foo"
    signature.outputs.inputs[0]._name = "bar"

    return signature


@pytest.fixture
def model_uri(tmp_path, dataset: tuple, model_signature: ModelSignature) -> str:
    X, y = dataset

    clf = DummyClassifier(strategy="prior")
    clf.fit(X, y)

    model_path = os.path.join(tmp_path, "dummy-model")
    mlflow.sklearn.save_model(clf, path=model_path, signature=model_signature)

    return model_path


@pytest.fixture
def pytorch_model_uri() -> str:
    pytorch_model_path = os.path.join(TESTDATA_PATH, "pytorch_model")
    if sys.version_info >= (3, 8):
        return os.path.join(pytorch_model_path, "3.8")

    return os.path.join(pytorch_model_path, "3.7")


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="mlflow-model",
        parameters=ModelParameters(uri=model_uri),
    )


@pytest.fixture
def model_settings_pytorch_fixed(pytorch_model_uri) -> ModelSettings:
    return ModelSettings(
        name="mlflow-model",
        parameters=ModelParameters(uri=pytorch_model_uri),
    )


@pytest.fixture
async def runtime(model_settings: ModelSettings) -> MLflowRuntime:
    model = MLflowRuntime(model_settings)
    await model.load()

    return model


@pytest.fixture
async def runtime_pytorch(model_settings_pytorch_fixed: ModelSettings) -> MLflowRuntime:
    model = MLflowRuntime(model_settings_pytorch_fixed)
    await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
