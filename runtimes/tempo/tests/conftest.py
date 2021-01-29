import os
import pytest
import numpy as np

from tempo.serve.pipeline import Pipeline
from tempo.serve.utils import pipeline
from tempo.seldon.docker import SeldonDockerRuntime
from tempo.kfserving.protocol import KFServingV2Protocol

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest, RequestInput

from mlserver_tempo import TempoModel


def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
def inference_pipeline() -> Pipeline:
    # NOTE: We define the class inside the scope of the fixture to make sure
    # that the serialisation works correctly.
    # This way, we simulate a remote host, without access to the actual class
    # definition.
    protocol = KFServingV2Protocol(model_name="test")
    runtime = SeldonDockerRuntime(protocol)

    @pipeline(
        name="inference-pipeline",
        runtime=runtime,
    )
    def _pipeline(payload: np.ndarray) -> np.ndarray:
        return payload.sum(keepdims=True)

    return _pipeline


@pytest.fixture
def pipeline_uri(inference_pipeline: Pipeline, tmp_path: str) -> str:
    file_path = os.path.join(tmp_path, "sum-pipeline.pickle")
    inference_pipeline.save(file_path)

    return file_path


@pytest.fixture
def model_settings(pipeline_uri: str) -> ModelSettings:
    return ModelSettings(
        name="sum-pipeline",
        parameters=ModelParameters(uri=pipeline_uri),
    )


@pytest.fixture
def inference_request() -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            RequestInput(name="input-0", shape=[4], data=[1, 2, 3, 4], datatype="FP32")
        ]
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> TempoModel:
    model = TempoModel(model_settings)
    await model.load()

    return model
