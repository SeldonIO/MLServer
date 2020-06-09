import pytest
import os

from mlserver.handlers import DataPlane
from mlserver.registry import ModelRegistry
from mlserver.model import Model
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


class SumModel(Model):
    name = "sum-model"

    def predict(self, payload: InferenceRequest) -> InferenceResponse:
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = ResponseOutput(name="total", shape=[1], datatype="INT32", data=[total])
        return InferenceResponse(model_name=self.name, id="1", outputs=[output])


@pytest.fixture
def sum_model() -> SumModel:
    return SumModel()


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)


@pytest.fixture
def model_registry(sum_model: SumModel) -> ModelRegistry:
    model_registry = ModelRegistry()
    model_registry.load(sum_model.name, sum_model)
    return model_registry


@pytest.fixture
def data_plane(model_registry: ModelRegistry) -> DataPlane:
    return DataPlane(model_registry=model_registry)
