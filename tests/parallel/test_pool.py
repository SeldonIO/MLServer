import os
import pytest
import asyncio
import numpy as np

from mlserver.errors import MLServerError
from mlserver.model import MLModel
from mlserver.settings import Settings
from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyCodec, StringCodec
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


async def test_on_worker_stop(
    settings: Settings, inference_pool: InferencePool, sum_model: MLModel
):
    # Ensure pool has some loaded models
    await inference_pool.load_model(sum_model)

    prev_workers = list(inference_pool._workers.values())
    stopped_worker = prev_workers[0]

    await inference_pool.on_worker_stop(stopped_worker.pid, 23)
    await stopped_worker.stop()

    # Make sure worker is taken out of the rota and a new worker is started
    new_workers = list(inference_pool._workers.values())
    assert len(new_workers) == settings.parallel_workers
    for worker in new_workers:
        assert worker.pid != stopped_worker.pid


async def test_start_worker(
    settings: Settings,
    inference_pool: InferencePool,
    sum_model: MLModel,
    inference_request: InferenceRequest,
):
    # Ensure pool has some loaded models
    model = await inference_pool.load_model(sum_model)

    # Assert no traffic errors while new worker is starting
    start_worker_task = asyncio.create_task(inference_pool._start_worker())
    while not start_worker_task.done():
        inference_response = await model.predict(inference_request)
        assert len(inference_response.outputs) == 1

    await start_worker_task

    # Make a last pass through all workers
    for _ in range(settings.parallel_workers + 2):
        inference_response = await model.predict(inference_request)
        assert len(inference_response.outputs) == 1


async def test_start_worker_new_model(
    settings: Settings,
    inference_pool: InferencePool,
    sum_model: MLModel,
    simple_model: MLModel,
):
    # Ensure pool has some loaded models
    await inference_pool.load_model(sum_model)

    # Assert new models make their way through to the new worker
    start_worker_task = asyncio.create_task(inference_pool._start_worker())
    new_model = await inference_pool.load_model(simple_model)
    inference_request = InferenceRequest(
        inputs=[
            NumpyCodec.encode_input("foo", np.array([[1, 2]], dtype=np.int32)),
            StringCodec.encode_input("bar", ["asd", "qwe"]),
        ]
    )
    while not start_worker_task.done():
        inference_response = await new_model.predict(inference_request)
        assert len(inference_response.outputs) == 1

    await start_worker_task

    # Make a last pass through all workers
    for _ in range(settings.parallel_workers + 2):
        inference_response = await new_model.predict(inference_request)
        assert len(inference_response.outputs) == 1


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
    assert len(inference_pool._worker_registry) == 0
    model = await inference_pool.load_model(sum_model)
    assert len(inference_pool._worker_registry) == 1

    # NOTE: This should leverage the worker inference_pool, after wrapping the
    # model
    inference_response = await model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model.settings.name
    assert len(inference_response.outputs) == 1

    await inference_pool.unload_model(sum_model)
    assert len(inference_pool._worker_registry) == 0


async def test_load_error(
    inference_pool: InferencePool,
    load_error_model: MLModel,
):
    assert len(inference_pool._worker_registry) == 0
    with pytest.raises(MLServerError) as excinfo:
        await inference_pool.load_model(load_error_model)

    assert len(inference_pool._worker_registry) == 0
    expected_msg = f"mlserver.errors.MLServerError: {ErrorModel.error_message}"
    assert str(excinfo.value) == expected_msg
