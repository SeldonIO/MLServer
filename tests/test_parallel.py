import pytest

from mlserver.parallel import (
    InferencePool,
    _InferencePoolAttr,
    load_inference_pool,
    unload_inference_pool,
    parallel,
)
from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse


@pytest.fixture
async def inference_pool(sum_model: MLModel) -> InferencePool:
    pool = InferencePool(sum_model)

    yield pool

    pool.__del__()


async def test_pool_load(
    inference_pool: InferencePool, inference_request: InferenceRequest
):
    executor = inference_pool._executor

    # Trigger a process scale up
    await inference_pool.predict(inference_request)

    executor._adjust_process_count()

    # TODO: Change once number of workers are configurable
    assert len(executor._processes) == 8


async def test_pool_predict(
    inference_pool: InferencePool, inference_request: InferenceRequest
):
    response = await inference_pool.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1


async def test_parallel_predict(
    sum_model: MLModel, inference_request: InferenceRequest
):
    await load_inference_pool(sum_model)
    response = await sum_model.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1


async def test_del(inference_pool: InferencePool, inference_request: InferenceRequest):
    executor = inference_pool._executor

    # Trigger a process scale up
    await inference_pool.predict(inference_request)

    inference_pool.__del__()

    assert executor._processes is None


async def test_load_inference_pool(sum_model: MLModel):
    await load_inference_pool(sum_model)

    assert hasattr(sum_model, _InferencePoolAttr)


async def test_unload_inference_pool(sum_model: MLModel):
    await load_inference_pool(sum_model)
    await unload_inference_pool(sum_model)

    assert not hasattr(sum_model, _InferencePoolAttr)
