import pytest
import os

from mlserver.handlers import DataPlane
from mlserver.registry import ModelRegistry
from mlserver import types, Settings

from .models import SumModel

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


@pytest.fixture
def sum_model() -> SumModel:
    return SumModel("sum-model", "1.2.3")


@pytest.fixture
def inference_request() -> types.InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return types.InferenceRequest.parse_file(payload_path)


@pytest.fixture
def inference_response() -> types.InferenceResponse:
    payload_path = os.path.join(TESTDATA_PATH, "inference-response.json")
    return types.InferenceResponse.parse_file(payload_path)


@pytest.fixture
def model_registry(sum_model: SumModel) -> ModelRegistry:
    model_registry = ModelRegistry()
    model_registry.load(sum_model.name, sum_model)
    return model_registry


@pytest.fixture
def settings() -> Settings:
    settings = Settings(debug=True)
    return settings


@pytest.fixture
def data_plane(settings: Settings, model_registry: ModelRegistry) -> DataPlane:
    return DataPlane(settings=settings, model_registry=model_registry)
