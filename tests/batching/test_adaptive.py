import asyncio

from mlserver.batching.adaptive import AdaptiveBatcher
from mlserver.model import MLModel

from .conftest import TestRequestSender


async def test_collect_requests(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
):
    max_batch_size = adaptive_batcher._max_batch_size
    send_request_coros = [send_request() for _ in range(max_batch_size)]
    coros = await asyncio.gather(
        adaptive_batcher._collect_requests(), *send_request_coros
    )

    collected_requests = coros[0]
    sent_requests = coros[1:]

    assert collected_requests == sent_requests


async def test_collect_requests_timeout(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
):
    collected_requests, sent_request = await asyncio.gather(
        adaptive_batcher._collect_requests(), send_request()
    )

    assert collected_requests == [sent_request]


async def test_batch_requests(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
    sum_model: MLModel,
):
    max_batch_size = adaptive_batcher._max_batch_size
    send_request_coros = [send_request() for _ in range(max_batch_size)]

    coros = await asyncio.gather(
        adaptive_batcher._batch_requests(), *send_request_coros
    )

    sent_requests = coros[1:]
    assert len(sent_requests) == len(adaptive_batcher._responses)

    for sent_request in sent_requests:
        assert sent_request.id in adaptive_batcher._responses

        expected = await sum_model.predict(sent_request)
        assert expected == adaptive_batcher._responses[sent_request.id]
