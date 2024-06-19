import os
import mlflow
import pytest
import asyncio
import numpy as np
import pandas as pd

from filelock import FileLock
from sklearn.dummy import DummyClassifier
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from mlflow.models.signature import ModelSignature, infer_signature
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver.utils import install_uvloop_event_loop

from mlserver_mlflow import MLflowRuntime

from .torch_fixtures import MNISTDataModule, LightningMNISTClassifier

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")
TESTDATA_CACHE_PATH = os.path.join(TESTDATA_PATH, ".cache")


@pytest.fixture
def event_loop():
    # By default use uvloop for tests
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def dataset() -> tuple:
    n = 4
    X = pd.DataFrame({"foo": np.random.rand(n)})
    y = np.random.rand(n)

    return X, y


@pytest.fixture
def default_inference_params() -> dict:
    return {"foo_param": "foo_value"}


@pytest.fixture
def model_signature(dataset: tuple, default_inference_params: dict) -> ModelSignature:
    X, y = dataset
    signature = infer_signature(X, model_output=y, params=default_inference_params)

    return signature


@pytest.fixture
def model_uri(tmp_path: str, dataset: tuple, model_signature: ModelSignature) -> str:
    X, y = dataset

    clf = DummyClassifier(strategy="prior")
    clf.fit(X, y)

    model_path = os.path.join(tmp_path, "dummy-model")
    mlflow.sklearn.save_model(clf, path=model_path, signature=model_signature)

    return model_path


@pytest.fixture
def testdata_cache_path() -> str:
    if not os.path.exists(TESTDATA_CACHE_PATH):
        os.makedirs(TESTDATA_CACHE_PATH, exist_ok=True)

    return TESTDATA_CACHE_PATH


@pytest.fixture
def pytorch_model_uri(
    testdata_cache_path: str,
) -> str:
    model_path = os.path.join(testdata_cache_path, "pytorch-model")

    # NOTE: Lock to avoid race conditions when running tests in parallel
    with FileLock(f"{model_path}.lock"):
        if os.path.exists(model_path):
            return model_path

        model = LightningMNISTClassifier(batch_size=64, num_workers=0, lr=0.001)

        dm = MNISTDataModule(batch_size=64, num_workers=0)
        dm.setup(stage="fit")

        early_stopping = EarlyStopping(
            monitor="val_loss",
            mode="min",
            verbose=False,
            patience=3,
        )

        trainer = Trainer(callbacks=[early_stopping])
        trainer.fit(model, dm)

        mlflow.pytorch.save_model(model, path=model_path)

    return model_path


@pytest.fixture(params=["", "file:"])
def model_settings(model_uri: str, request: pytest.FixtureRequest) -> ModelSettings:
    scheme = request.param
    model_uri = scheme + model_uri
    return ModelSettings(
        name="mlflow-model",
        implementation=MLflowRuntime,
        parameters=ModelParameters(uri=model_uri),
    )


@pytest.fixture
def model_settings_pytorch_fixed(pytorch_model_uri) -> ModelSettings:
    return ModelSettings(
        name="mlflow-model",
        implementation=MLflowRuntime,
        parameters=ModelParameters(uri=pytorch_model_uri),
    )


@pytest.fixture
async def runtime(model_settings: ModelSettings) -> MLflowRuntime:
    model = MLflowRuntime(model_settings)
    model.ready = await model.load()

    return model


@pytest.fixture
async def runtime_pytorch(model_settings_pytorch_fixed: ModelSettings) -> MLflowRuntime:
    model = MLflowRuntime(model_settings_pytorch_fixed)
    model.ready = await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
