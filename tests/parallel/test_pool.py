import os

from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest
from mlserver.parallel.pool import InferencePool


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


def test_workers_start(pool: InferencePool):
    # TODO: Read number of workers from settings
    assert len(pool._workers) == 4

    for worker_pid in pool._workers:
        assert check_pid(worker_pid)


async def test_close(pool: InferencePool):
    worker_pids = [pid for pid in pool._workers]

    await pool.close()

    assert len(pool._workers) == 0
    for worker_pid in worker_pids:
        assert not check_pid(worker_pid)


async def test_load(
    pool: InferencePool, sum_model: MLModel, inference_request: InferenceRequest
):
    sum_model.settings.name = "foo"
    await pool.load_model(sum_model)

    # NOTE: This should leverage the worker pool, after decorating the method
    inference_response = await sum_model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model.settings.name
    assert len(inference_response.outputs) == 1


async def test_predict(
    pool: InferencePool,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    inference_response = await pool.predict(sum_model_settings, inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model_settings.name
    assert len(inference_response.outputs) == 1
