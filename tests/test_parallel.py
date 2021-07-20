import pytest

from mlserver.parallel import ParallelRuntime
from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse


@pytest.fixture
def parallel_runtime(sum_model: MLModel) -> ParallelRuntime:
    return ParallelRuntime(sum_model)


async def test_load(parallel_runtime):
    await parallel_runtime.load()

    # TODO: Assert that loop is created
    assert parallel_runtime._executor is not None


async def test_predict(parallel_runtime, inference_request: InferenceRequest):
    await parallel_runtime.load()

    response = await parallel_runtime.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1
