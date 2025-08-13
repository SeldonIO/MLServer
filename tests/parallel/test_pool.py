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

# --- Add these imports at the top of the file (with the others) ---
from typing import List
from mlserver.parallel.dispatcher import Dispatcher
from mlserver.parallel.messages import (
    ModelRequestMessage,
    ModelResponseMessage,
    ModelStreamChunkMessage,
    ModelStreamEndMessage,
)
from mlserver.parallel.model import ModelMethods
from mlserver.utils import generate_uuid
from mlserver.parallel.worker import Worker  # for monkeypatching in stream tests



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

@pytest.mark.asyncio
async def test_streaming_success_and_error_demux(
    inference_pool: InferencePool,
    sum_model: MLModel,
    sum_model_settings,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    Exercise the streaming demux in the dispatcher:
      - One request that yields two chunks and ends OK.
      - One request that yields a chunk then terminates with an error.
    We simulate worker output by pushing messages into the shared responses queue
    and *prevent the real worker* from trying to execute unknown methods by
    patching Worker.send_request to a no-op.
    """
    # Load a model (not strictly used by the fake streaming method, but keeps pool in a normal state)
    await inference_pool.load_model(sum_model)
    dispatcher: Dispatcher = inference_pool._dispatcher

    # Prevent real worker RPC for our fake streaming methods
    monkeypatch.setattr(Worker, "send_request", lambda self, msg: None, raising=True)

    # --- Success case ---
    stream_ok = ModelRequestMessage(
        id=generate_uuid(),
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name="stream_ok",
        method_args=[],
        method_kwargs={},
    )
    agen_ok = await dispatcher.dispatch_request_stream(stream_ok)
    await asyncio.sleep(0)  # let per-request queue be created

    dispatcher._responses.put(ModelStreamChunkMessage(id=stream_ok.id, chunk=b"a"))
    dispatcher._responses.put(ModelStreamChunkMessage(id=stream_ok.id, chunk=b"b"))
    dispatcher._responses.put(ModelStreamEndMessage(id=stream_ok.id))
    # minimal unary ack so the scheduled future resolves
    dispatcher._responses.put(ModelResponseMessage(id=stream_ok.id, return_value=None))

    seen_ok: List[bytes] = []
    async for ch in agen_ok:
        seen_ok.append(ch)

    # Order can be racy on some platforms; accept set equality to avoid flakiness
    assert set(seen_ok) == {b"a", b"b"}
    assert stream_ok.id not in dispatcher._async_responses._streams

    # --- Error case ---
    stream_err = ModelRequestMessage(
        id=generate_uuid(),
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name="stream_err",
        method_args=[],
        method_kwargs={},
    )
    agen_err = await dispatcher.dispatch_request_stream(stream_err)
    await asyncio.sleep(0)

    dispatcher._responses.put(ModelStreamChunkMessage(id=stream_err.id, chunk=b"x"))
    dispatcher._responses.put(
        ModelStreamEndMessage(id=stream_err.id, exception=RuntimeError("boom"))
    )
    dispatcher._responses.put(ModelResponseMessage(id=stream_err.id, return_value=None))

    first = await agen_err.__anext__()
    assert first == b"x"
    with pytest.raises(RuntimeError) as err:
        await agen_err.__anext__()
    assert "boom" in str(err.value)
    assert stream_err.id not in dispatcher._async_responses._streams


@pytest.mark.asyncio
async def test_two_workers_and_distribution(
    inference_pool: InferencePool,
    sum_model: MLModel,
    sum_model_settings,
    inference_request: InferenceRequest,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    Ensure we really have 2 workers and requests get distributed across both.
    We spy on the internal assignment path.
    """
    # Load a model (so Metadata calls can be handled by workers)
    await inference_pool.load_model(sum_model)
    dispatcher: Dispatcher = inference_pool._dispatcher

    assert len(inference_pool._workers) == 2  # parallel_workers should be 2

    assigned_pids: List[int] = []
    real_track = dispatcher._async_responses._track_message

    def _spy_track(msg, worker):
        assigned_pids.append(worker.pid)  # type: ignore[attr-defined]
        return real_track(msg, worker)

    monkeypatch.setattr(
        dispatcher._async_responses, "_track_message", _spy_track, raising=True
    )

    # Fire a handful of metadata requests
    reqs = [
        ModelRequestMessage(
            id=generate_uuid(),
            model_name=sum_model_settings.name,
            model_version=sum_model_settings.parameters.version,
            method_name=ModelMethods.Metadata.value,
            method_args=[],
            method_kwargs={},
        )
        for _ in range(8)
    ]
    res = await asyncio.gather(*[dispatcher.dispatch_request(r) for r in reqs])

    assert all(r.exception is None for r in res)
    # We should see both worker PIDs in the assignment log
    assert len(set(assigned_pids)) == 2


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

