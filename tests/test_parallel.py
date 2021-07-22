import pytest

from mlserver.parallel import ParallelRuntime
from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse


@pytest.fixture
async def parallel_runtime(sum_model: MLModel) -> ParallelRuntime:
    runtime = ParallelRuntime(sum_model)
    await runtime.load()

    yield runtime

    runtime.__del__()


async def test_load(parallel_runtime):
    executor = parallel_runtime._executor

    executor._adjust_process_count()

    # TODO: Change once number of workers are configurable
    assert len(executor._processes) == 8


async def test_predict(parallel_runtime, inference_request: InferenceRequest):
    response = await parallel_runtime.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1


async def test_del(parallel_runtime):
    executor = parallel_runtime._executor
    executor._adjust_process_count()

    parallel_runtime.__del__()

    assert executor._processes is None
