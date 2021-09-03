import asyncio

from mlserver.batching.adaptive import AdaptiveBatcher
from mlserver.types import InferenceRequest, RequestInput
from mlserver.model import MLModel

from .conftest import TestRequestSender


async def test_batch_requests(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
):
    max_batch_size = adaptive_batcher._max_batch_size
    sent_requests = await asyncio.gather(
        *[send_request() for _ in range(max_batch_size)]
    )
    batched_requests = [
        batched_req async for batched_req in adaptive_batcher._batch_requests()
    ]

    assert len(batched_requests) == 1
    assert batched_requests[0]._inference_requests == sent_requests


async def test_batch_requests_timeout(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
):

    sent_request = await send_request()
    batched_requests = [
        batched_req async for batched_req in adaptive_batcher._batch_requests()
    ]

    assert len(batched_requests) == 1
    assert batched_requests[0]._inference_requests == [sent_request]


async def test_batcher(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
    sum_model: MLModel,
):
    max_batch_size = adaptive_batcher._max_batch_size
    sent_requests = await asyncio.gather(
        *[send_request() for _ in range(max_batch_size)]
    )

    await adaptive_batcher._batcher()

    assert len(sent_requests) == len(adaptive_batcher._async_responses)

    for sent_request in sent_requests:
        async_response = adaptive_batcher._async_responses[sent_request.id]
        assert async_response.done()

        response = await async_response
        assert sent_request.id == response.id

        expected = await sum_model.predict(sent_request)
        assert expected == response


async def test_predict(adaptive_batcher: AdaptiveBatcher, sum_model: MLModel):
    # Make sure that one "batch" is only half-full
    num_requests = adaptive_batcher._max_batch_size * 2 + 2
    requests = [
        InferenceRequest(
            id=f"request-{idx}",
            inputs=[
                RequestInput(
                    name="input-0",
                    shape=[1, 3],
                    datatype="INT32",
                    data=[idx, idx + 1, idx + 2],
                )
            ],
        )
        for idx in range(num_requests)
    ]

    responses = await asyncio.gather(
        *[adaptive_batcher.predict(request) for request in requests]
    )

    assert len(requests) == len(responses)
    for req, res in zip(requests, responses):
        assert req.id == res.id

        expected = await sum_model.predict(req)
        assert res == expected
