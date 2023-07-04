import pytest

from mlserver.types import InferenceResponse
from mlserver.parallel.errors import WorkerStop
from mlserver.parallel.dispatcher import Dispatcher
from mlserver.parallel.messages import ModelUpdateMessage, ModelRequestMessage


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


async def test_dispatch(
    dispatcher: Dispatcher,
    load_message: ModelUpdateMessage,
    inference_request_message: ModelRequestMessage,
):
    await dispatcher.dispatch_update(load_message)
    response_message = await dispatcher.dispatch_request(inference_request_message)

    assert response_message.exception is None
    inference_response = response_message.return_value
    assert isinstance(inference_response, InferenceResponse)
    assert len(inference_response.outputs) > 0


async def test_cancel(dispatcher: Dispatcher, inference_request_message):
    worker = list(dispatcher._workers.values())[0]
    async_responses = dispatcher._async_responses
    async_responses._schedule(inference_request_message, worker)

    exit_code = 234
    async_responses.cancel(worker, exit_code)

    with pytest.raises(WorkerStop) as err:
        await async_responses._wait(inference_request_message.id)

    assert str(exit_code) in str(err)
