import asyncio
import pytest
from typing import List
from mlserver.parallel.errors import WorkerStop
from mlserver.parallel.dispatcher import Dispatcher
from mlserver.parallel.messages import (
    ModelRequestMessage,
    ModelResponseMessage,
    ModelStreamChunkMessage,
    ModelStreamEndMessage,
)


async def test_on_worker_stop(dispatcher: Dispatcher):
    worker = list(dispatcher._workers.values())[0]
    await worker.stop()
    dispatcher.on_worker_stop(worker, 255)

    assert worker.pid not in dispatcher._workers
    # Ensure worker is no longer in round robin rotation
    workers_count = len(dispatcher._workers)
    for _ in range(workers_count + 1):
        worker_pid = next(dispatcher._workers_round_robin)
        assert worker_pid != worker.pid


async def test_cancel(
    dispatcher: Dispatcher, inference_request_message: ModelRequestMessage
):
    worker = list(dispatcher._workers.values())[0]
    async_responses = dispatcher._async_responses
    async_responses._schedule(inference_request_message, worker)

    exit_code = 234
    async_responses.cancel(worker, exit_code)

    with pytest.raises(WorkerStop) as err:
        await async_responses._wait(inference_request_message.id)

    assert str(exit_code) in str(err)


# --- SUCCESSFUL STREAM --------------------------------------------------------


async def test_dispatch_streaming(
    dispatcher: Dispatcher,
    inference_request_message: ModelRequestMessage,
):
    # Build a streaming request (method name is arbitrary for this simulation)
    stream_req = ModelRequestMessage(
        model_name=inference_request_message.model_name,
        model_version=inference_request_message.model_version,
        method_name="stream_tokens",
        method_args=[],
        method_kwargs={},
    )

    # Simulate the worker pushing messages into the shared responses queue.
    # IMPORTANT: use the SAME id as the request.
    async def feeder():
        await asyncio.sleep(0)  # let dispatch_request_stream set up its queue
        dispatcher._responses.put(ModelStreamChunkMessage(id=stream_req.id, chunk=b"a"))
        dispatcher._responses.put(ModelStreamChunkMessage(id=stream_req.id, chunk=b"b"))
        dispatcher._responses.put(ModelStreamEndMessage(id=stream_req.id))
        # Minimal unary ack so the scheduled future resolves
        dispatcher._responses.put(
            ModelResponseMessage(id=stream_req.id, return_value=None)
        )

    asyncio.create_task(feeder())

    chunks: List[bytes] = []
    stream_iter = await dispatcher.dispatch_request_stream(stream_req)
    async for ch in stream_iter:
        chunks.append(ch)

    assert chunks == [b"a", b"b"]


# --- ERRORING STREAM ----------------------------------------------------------


async def test_dispatch_streaming_error(
    dispatcher: Dispatcher,
    inference_request_message: ModelRequestMessage,
):
    stream_req = ModelRequestMessage(
        model_name=inference_request_message.model_name,
        model_version=inference_request_message.model_version,
        method_name="stream_tokens_err",
        method_args=[],
        method_kwargs={},
    )

    async def feeder():
        await asyncio.sleep(0)  # let the dispatcher set up its per-request queue
        dispatcher._responses.put(ModelStreamChunkMessage(id=stream_req.id, chunk=b"x"))
        # Use a BUILT-IN exception so it's picklable across multiprocessing.Queue
        dispatcher._responses.put(
            ModelStreamEndMessage(
                id=stream_req.id, exception=RuntimeError("fail mid-stream")
            )
        )
        # Minimal unary ack so the scheduled future resolves
        dispatcher._responses.put(
            ModelResponseMessage(id=stream_req.id, return_value=None)
        )

    asyncio.create_task(feeder())

    stream_iter = await dispatcher.dispatch_request_stream(stream_req)

    # First chunk arrives
    first = await stream_iter.__anext__()
    assert first == b"x"

    # Next iteration raises the error propagated via END message
    with pytest.raises(RuntimeError) as err:
        await stream_iter.__anext__()

    assert "fail mid-stream" in str(err.value)
