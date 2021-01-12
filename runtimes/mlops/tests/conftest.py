import os
import pytest
import pickle
import numpy as np

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest, RequestInput

from mlserver_mlops import MLOpsModel


class SumPipeline(object):
    def pipeline(self, request: np.array) -> np.array:
        return np.array([request.sum()])


def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
def pipeline() -> SumPipeline:
    return SumPipeline()


@pytest.fixture
def pipeline_uri(pipeline: SumPipeline, tmp_path: str) -> str:
    file_path = os.path.join(tmp_path, "sum-pipeline.pickle")
    with open(file_path, "wb") as file:
        pickle.dump(pipeline, file)

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
async def model(model_settings: ModelSettings) -> MLOpsModel:
    model = MLOpsModel(model_settings)
    await model.load()

    return model
