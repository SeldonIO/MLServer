import os
import pytest

from mlserver.errors import MLServerError
from mlserver.model import MLModel
from mlserver.settings import Settings
from mlserver.types import InferenceRequest
from mlserver.parallel.pool import InferencePool

from ..fixtures import ErrorModel

from ..metrics.conftest import prometheus_registry
from prometheus_client.registry  import CollectorRegistry

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


def test_workers_start(prometheus_registry: CollectorRegistry, inference_pool: InferencePool,  settings: Settings):
    assert len(inference_pool._workers) == settings.parallel_workers

    for worker_pid in inference_pool._workers:
        assert check_pid(worker_pid)


async def test_close(prometheus_registry: CollectorRegistry, inference_pool: InferencePool):
    worker_pids = [pid for pid in inference_pool._workers]

    await inference_pool.close()

    assert len(inference_pool._workers) == 0
    for worker_pid in worker_pids:
        assert not check_pid(worker_pid)


async def test_load(
    prometheus_registry: CollectorRegistry,
    inference_pool: InferencePool,
    sum_model: MLModel,
    inference_request: InferenceRequest,
):
    sum_model.settings.name = "foo"
    model = await inference_pool.load_model(sum_model)

    # NOTE: This should leverage the worker inference_pool, after wrapping the
    # model
    inference_response = await model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model.settings.name
    assert len(inference_response.outputs) == 1


async def test_load_error(
    prometheus_registry: CollectorRegistry,
    inference_pool: InferencePool,
    load_error_model: MLModel,
):
    with pytest.raises(MLServerError) as excinfo:
        await inference_pool.load_model(load_error_model)

    assert str(excinfo.value) == ErrorModel.error_message
