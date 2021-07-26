import pytest

from mlserver.parallel import InferencePool
from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse


@pytest.fixture
async def inference_pool(sum_model: MLModel) -> InferencePool:
    pool = InferencePool(sum_model)

    yield pool

    pool.__del__()


async def test_load(inference_pool: InferencePool):
    executor = inference_pool._executor

    executor._adjust_process_count()

    # TODO: Change once number of workers are configurable
    assert len(executor._processes) == 8


async def test_predict(
    inference_pool: InferencePool, inference_request: InferenceRequest
):
    response = await inference_pool.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1


async def test_del(inference_pool: InferencePool):
    executor = inference_pool._executor
    executor._adjust_process_count()

    inference_pool.__del__()

    assert executor._processes is None
