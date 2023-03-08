import os
import pytest

from mlserver.errors import MLServerError
from mlserver.model import MLModel
from mlserver.settings import Settings
from mlserver.types import InferenceRequest
from mlserver.parallel.pool import InferencePool

from ..fixtures import ErrorModel


def check_pid(pid):
    """
    Check For the existence of a unix pid.

    From https://stackoverflow.com/a/568285/5015573
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def test_workers_start(inference_pool: InferencePool, settings: Settings):
    assert len(inference_pool._workers) == settings.parallel_workers

    for worker_pid in inference_pool._workers:
        assert check_pid(worker_pid)


async def test_close(inference_pool: InferencePool):
    worker_pids = [pid for pid in inference_pool._workers]

    await inference_pool.close()

    assert len(inference_pool._workers) == 0
    for worker_pid in worker_pids:
        assert not check_pid(worker_pid)


async def test_load(
    inference_pool: InferencePool,
    sum_model: MLModel,
    inference_request: InferenceRequest,
):
    sum_model.settings.name = "foo"
    assert inference_pool._model_count == 0
    model = await inference_pool.load_model(sum_model)
    assert inference_pool._model_count == 1

    # NOTE: This should leverage the worker inference_pool, after wrapping the
    # model
    inference_response = await model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model.settings.name
    assert len(inference_response.outputs) == 1

    await inference_pool.unload_model(sum_model)
    assert inference_pool._model_count == 0


async def test_load_error(
    inference_pool: InferencePool,
    load_error_model: MLModel,
):
    assert inference_pool._model_count == 0
    with pytest.raises(MLServerError) as excinfo:
        await inference_pool.load_model(load_error_model)

    assert inference_pool._model_count == 0
    expected_msg = f"mlserver.errors.MLServerError: {ErrorModel.error_message}"
    assert str(excinfo.value) == expected_msg
