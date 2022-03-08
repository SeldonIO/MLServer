import os
import mlflow
import pytest
import numpy as np

from sklearn.dummy import DummyClassifier
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from mlflow.models.signature import ModelSignature, infer_signature
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

from mlserver_mlflow import MLflowRuntime

from torch_fixtures import MNISTDataModule, LightningMNISTClassifier

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")
TESTDATA_CACHE_PATH = os.path.join(TESTDATA_PATH, ".cache")


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


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="mlflow-model",
        implementation=MLflowRuntime,
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
