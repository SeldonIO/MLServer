import os
import mlflow
import pytest
import asyncio
import numpy as np
import pandas as pd
from typing import Iterable
from sklearn.dummy import DummyClassifier
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from mlflow.models.signature import ModelSignature, infer_signature
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver.utils import install_uvloop_event_loop

from mlserver_mlflow import MLflowRuntime

from .torch_fixtures import MNISTDataModule, LightningMNISTClassifier

from prometheus_client.registry import REGISTRY
from starlette_exporter import PrometheusMiddleware

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")
TESTDATA_CACHE_PATH = os.path.join(TESTDATA_PATH, ".cache")


@pytest.fixture(autouse=True)
def prometheus_registry() -> Iterable:
    """
    Fixture used to ensure the registry is cleaned on each run.
    Otherwise, `py-grpc-prometheus` will complain that metrics already exist.

    TODO: Open issue in `py-grpc-prometheus` to check whether a metric exists
    before creating it.
    For an example on how to do this, see `starlette_exporter`'s implementation

        https://github.com/stephenhillier/starlette_exporter/blob/947d4d631dd9a6a8c1071b45573c5562acba4834/starlette_exporter/middleware.py#L67
    """
    # NOTE: Since the `REGISTRY` object is global, this fixture is NOT
    # thread-safe!!
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)

    # Clean metrics from `starlette_exporter` as well, as otherwise they won't
    # get re-created
    PrometheusMiddleware._metrics.clear()

    yield REGISTRY


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
def model_signature(dataset: tuple) -> ModelSignature:
    X, y = dataset
    signature = infer_signature(X, y)

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
def pytorch_model_uri() -> str:
    model_path = os.path.join(TESTDATA_CACHE_PATH, "pytorch-model")
    if os.path.exists(model_path):
        return model_path

    model = LightningMNISTClassifier(batch_size=64, num_workers=3, lr=0.001)

    dm = MNISTDataModule(batch_size=64, num_workers=3)
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
