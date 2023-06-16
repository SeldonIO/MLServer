import pytest
import os

from mlserver import MLModel, MLServer, ModelSettings

from ..conftest import TESTDATA_PATH
from ..fixtures import EchoModel


@pytest.fixture()
def single_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "single.txt")


@pytest.fixture()
def bytes_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "bytes.txt")


@pytest.fixture()
def invalid_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "invalid.txt")


@pytest.fixture()
def invalid_among_many():
    return os.path.join(TESTDATA_PATH, "batch_processing", "invalid_among_many.txt")


@pytest.fixture()
def many_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "many.txt")


@pytest.fixture()
def single_input_with_id():
    return os.path.join(TESTDATA_PATH, "batch_processing", "single_with_id.txt")


@pytest.fixture
async def echo_model(mlserver: MLServer) -> MLModel:
    model_settings = ModelSettings(name="echo-model", implementation=EchoModel)
    return await mlserver._model_registry.load(model_settings)
