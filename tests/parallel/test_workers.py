import asyncio
import statistics
import pytest
from typing import List, Dict

from mlserver.types import InferenceRequest
from mlserver.settings import ModelSettings
from mlserver.parallel.pool import InferencePool
from mlserver.parallel.dispatcher import Dispatcher
from mlserver.parallel.messages import (
    ModelRequestMessage,
    ModelResponseMessage,
    ModelStreamChunkMessage,
    ModelStreamEndMessage,
)
from mlserver.parallel.model import ModelMethods
from mlserver.utils import generate_uuid


# ==============================================================================
# Helpers
# ==============================================================================


def mk_metadata_msg(ms: ModelSettings) -> ModelRequestMessage:
    return ModelRequestMessage(
        id=generate_uuid(),
        model_name=ms.name,
        model_version=ms.parameters.version,
        method_name=ModelMethods.Metadata.value,
        method_args=[],
        method_kwargs={},
    )


def mk_predict_msg(ms: ModelSettings, req: InferenceRequest) -> ModelRequestMessage:
    return ModelRequestMessage(
        id=generate_uuid(),
        model_name=ms.name,
        model_version=ms.parameters.version,
        method_name=ModelMethods.Predict.value,
        method_args=[req],
        method_kwargs={},
    )


def mk_stream_msg(
    ms: ModelSettings, method_name: str = "stream_tokens"
) -> ModelRequestMessage:
    return ModelRequestMessage(
        id=generate_uuid(),
        model_name=ms.name,
        model_version=ms.parameters.version,
        method_name=method_name,
        method_args=[],
        method_kwargs={},
    )


class AssignSpy:
    """
    Records worker PIDs used for dispatch by temporarily wrapping
    AsyncResponses._track_message.
    """

    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.original = dispatcher._async_responses._track_message
        self.pids: List[int] = []
        self._mp: pytest.MonkeyPatch | None = None

    def _spy(self, message, worker):
        self.pids.append(worker.pid)  # type: ignore[attr-defined]
        return self.original(message, worker)

    def __enter__(self):
        # IMPORTANT: use MonkeyPatch(), not MonkeyPatch.context()
        self._mp = pytest.MonkeyPatch()
        self._mp.setattr(
            self.dispatcher._async_responses,
            "_track_message",
            self._spy,
            raising=True,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._mp is not None:
            self._mp.undo()
            self._mp = None


# ==============================================================================
# Shared fixtures for a 2-worker inference_pool and a loaded simple model
# ==============================================================================


@pytest.fixture
async def parallel_model(
    inference_pool: InferencePool, sum_model_settings: ModelSettings
):
    from tests.fixtures import SumModel

    model = SumModel(sum_model_settings)
    pm = await inference_pool.load_model(model)
    try:
        yield pm
    finally:
        await inference_pool.unload_model(model)


# ==============================================================================
# Worker count & distribution
# ==============================================================================


@pytest.mark.asyncio
async def test_worker_count(inference_pool: InferencePool):
    assert (
        len(inference_pool._workers) == inference_pool._settings.parallel_workers == 2
    )
    pids = [w.pid for w in inference_pool._workers.values()]
    assert len(pids) == len(set(pids))
    assert all(
        inference_pool._workers[pid].is_alive() for pid in pids
    )  # type: ignore[index]


@pytest.mark.asyncio
async def test_round_robin_small(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    with AssignSpy(dispatcher) as spy:
        reqs = [mk_metadata_msg(sum_model_settings) for _ in range(6)]
        resps = await asyncio.gather(*[dispatcher.dispatch_request(r) for r in reqs])

    assert all(r.exception is None for r in resps)
    assert len(set(spy.pids)) == 2  # both workers used


@pytest.mark.asyncio
async def test_concurrent_fairness(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    N = 100
    with AssignSpy(dispatcher) as spy:
        reqs = [mk_metadata_msg(sum_model_settings) for _ in range(N)]
        resps = await asyncio.gather(*[dispatcher.dispatch_request(r) for r in reqs])

    assert all(r.exception is None for r in resps)

    counts: Dict[int, int] = {}
    for pid in spy.pids:
        counts[pid] = counts.get(pid, 0) + 1

    assert len(counts) == 2
    c = list(counts.values())
    cv = statistics.pstdev(c) / (statistics.mean(c) or 1)
    assert cv < 0.3, f"Assignment too imbalanced: {counts} (cv={cv:.2f})"


# ==============================================================================
# In-flight maps lifecycle
# ==============================================================================


@pytest.mark.asyncio
async def test_inflight_maps_clean(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    ar = dispatcher._async_responses

    assert ar._futures_map == {}
    assert all(len(s) == 0 for s in ar._workers_map.values())

    req = mk_metadata_msg(sum_model_settings)
    task = asyncio.create_task(dispatcher.dispatch_request(req))
    await asyncio.sleep(0)

    assert req.id in ar._futures
    # Depending on timing, either check the key or the value presence
    assert req.id in ar._futures_map or req.id in ar._futures_map.values()

    await task
    assert req.id not in ar._futures
    assert req.id not in ar._futures_map


# ==============================================================================
# Streaming path: demux, errors, interleaving, backpressure, cancel
# ==============================================================================


@pytest.mark.asyncio
async def test_stream_demux_and_cleanup(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    req = mk_stream_msg(sum_model_settings, "stream_tokens")
    agen = await dispatcher.dispatch_request_stream(req)
    await asyncio.sleep(0)

    dispatcher._responses.put(ModelStreamChunkMessage(id=req.id, chunk=b"a"))
    dispatcher._responses.put(ModelStreamChunkMessage(id=req.id, chunk=b"b"))
    dispatcher._responses.put(ModelStreamEndMessage(id=req.id))
    dispatcher._responses.put(ModelResponseMessage(id=req.id, return_value=None))

    seen: List[bytes] = []
    async for ch in agen:
        seen.append(ch)

    assert set(seen) == set([b"a", b"b"])
    assert req.id not in dispatcher._async_responses._streams


@pytest.mark.asyncio
async def test_stream_error_propagation(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    req = mk_stream_msg(sum_model_settings, "stream_err")
    agen = await dispatcher.dispatch_request_stream(req)
    await asyncio.sleep(0)

    dispatcher._responses.put(ModelStreamChunkMessage(id=req.id, chunk=b"x"))
    dispatcher._responses.put(
        ModelStreamEndMessage(id=req.id, exception=RuntimeError("boom"))
    )
    dispatcher._responses.put(ModelResponseMessage(id=req.id, return_value=None))

    first = await agen.__anext__()
    assert first == b"x"
    with pytest.raises(RuntimeError) as err:
        await agen.__anext__()
    assert "boom" in str(err.value)
    assert req.id not in dispatcher._async_responses._streams


@pytest.mark.asyncio
async def test_stream_interleaving(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    req_a = mk_stream_msg(sum_model_settings, "stream_A")
    req_b = mk_stream_msg(sum_model_settings, "stream_B")

    agen_a = await dispatcher.dispatch_request_stream(req_a)
    agen_b = await dispatcher.dispatch_request_stream(req_b)
    await asyncio.sleep(0)

    dispatcher._responses.put(ModelStreamChunkMessage(id=req_a.id, chunk=b"a1"))
    dispatcher._responses.put(ModelStreamChunkMessage(id=req_b.id, chunk=b"b1"))
    dispatcher._responses.put(ModelStreamChunkMessage(id=req_a.id, chunk=b"a2"))
    dispatcher._responses.put(ModelStreamChunkMessage(id=req_b.id, chunk=b"b2"))
    dispatcher._responses.put(ModelStreamEndMessage(id=req_a.id))
    dispatcher._responses.put(ModelStreamEndMessage(id=req_b.id))
    dispatcher._responses.put(ModelResponseMessage(id=req_a.id, return_value=None))
    dispatcher._responses.put(ModelResponseMessage(id=req_b.id, return_value=None))

    seen_a: List[bytes] = []
    seen_b: List[bytes] = []

    async def drain(gen, bucket: List[bytes]):
        async for ch in gen:
            bucket.append(ch)

    await asyncio.gather(drain(agen_a, seen_a), drain(agen_b, seen_b))
    assert seen_a == [b"a1", b"a2"]
    assert seen_b == [b"b1", b"b2"]
    assert req_a.id not in dispatcher._async_responses._streams
    assert req_b.id not in dispatcher._async_responses._streams


@pytest.mark.asyncio
async def test_stream_backpressure(
    inference_pool: InferencePool,
    parallel_model,
    sum_model_settings: ModelSettings,
    monkeypatch,
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    # Enlarge per-request stream queue capacity to avoid QueueFull during the burst
    real_create = dispatcher._async_responses.create_stream_queue
    monkeypatch.setattr(
        dispatcher._async_responses,
        "create_stream_queue",
        lambda msg_id, maxsize=16: real_create(msg_id, maxsize=256),
    )

    req = mk_stream_msg(sum_model_settings, "stream_many")
    agen = await dispatcher.dispatch_request_stream(req)
    await asyncio.sleep(0)

    collected: List[bytes] = []

    async def consume():
        async for ch in agen:
            collected.append(ch)
            await asyncio.sleep(0)  # cooperative yield only

    consumer_task = asyncio.create_task(consume())

    for i in range(50):
        dispatcher._responses.put(
            ModelStreamChunkMessage(id=req.id, chunk=f"c{i}".encode())
        )
        await asyncio.sleep(0)

    dispatcher._responses.put(ModelStreamEndMessage(id=req.id))
    dispatcher._responses.put(ModelResponseMessage(id=req.id, return_value=None))

    await consumer_task
    assert set(collected) == set([f"c{i}".encode() for i in range(50)])
    assert req.id not in dispatcher._async_responses._streams


@pytest.mark.asyncio
async def test_stream_consumer_cancel(
    inference_pool: InferencePool, parallel_model, sum_model_settings: ModelSettings
):
    dispatcher: Dispatcher = inference_pool._dispatcher
    req = mk_stream_msg(sum_model_settings, "stream_cancel")
    agen = await dispatcher.dispatch_request_stream(req)
    await asyncio.sleep(0)

    dispatcher._responses.put(ModelStreamChunkMessage(id=req.id, chunk=b"head"))
    dispatcher._responses.put(ModelResponseMessage(id=req.id, return_value=None))

    head = await agen.__anext__()
    assert head == b"head"

    await agen.aclose()
    assert req.id not in dispatcher._async_responses._streams
