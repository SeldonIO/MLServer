import asyncio
import pytest

from typing import List

from mlserver.batching.adaptive import AdaptiveBatcher
from mlserver.batching.shape import Shape
from mlserver.types import InferenceRequest, RequestInput
from mlserver.model import MLModel

from .conftest import TestRequestSender


async def test_batch_requests(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
):
    max_batch_size = adaptive_batcher._max_batch_size
    sent_requests = dict(
        await asyncio.gather(*[send_request() for _ in range(max_batch_size)])
    )

    batched_requests = [
        batched_req async for batched_req in adaptive_batcher._batch_requests()
    ]

    assert len(batched_requests) == 1
    assert batched_requests[0].inference_requests == sent_requests


async def test_batch_requests_timeout(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
):
    """
    Test that a batch size smaller than the max batch size, the timeout is hit
    and the request gets processed.
    """
    for _ in range(2):
        sent_request = dict([await send_request()])
        batched_requests = [
            batched_req async for batched_req in adaptive_batcher._batch_requests()
        ]

        assert len(batched_requests) == 1
        assert batched_requests[0].inference_requests == sent_request


async def test_batcher(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
    sum_model: MLModel,
):
    max_batch_size = adaptive_batcher._max_batch_size
    sent_requests = dict(
        await asyncio.gather(*[send_request() for _ in range(max_batch_size)])
    )

    await adaptive_batcher._batcher()

    assert sent_requests.keys() == adaptive_batcher._async_responses.keys()

    for internal_id, sent_request in sent_requests.items():
        async_response = adaptive_batcher._async_responses[internal_id]
        assert async_response.done()

        response = await async_response
        assert sent_request.id == response.id

        expected = await sum_model.predict(sent_request)
        assert expected == response


async def test_batcher_propagates_errors(
    adaptive_batcher: AdaptiveBatcher,
    send_request: TestRequestSender,
    mocker,
):
    message = "This is an error"

    async def _async_exception():
        raise Exception(message)

    max_batch_size = adaptive_batcher._max_batch_size
    sent_requests = dict(
        await asyncio.gather(*[send_request() for _ in range(max_batch_size)])
    )

    adaptive_batcher._predict_fn = mocker.stub("predict")
    adaptive_batcher._predict_fn.return_value = _async_exception()
    await adaptive_batcher._batcher()

    for internal_id, _ in sent_requests.items():
        with pytest.raises(Exception) as err:
            await adaptive_batcher._async_responses[internal_id]

        assert str(err.value) == message


@pytest.mark.parametrize(
    "requests",
    [
        [
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
            # 10 is the max_batch_size for sum_model
            # Make sure one batch is only half-full
            for idx in range(10 * 2 + 2)
        ],
        [
            InferenceRequest(
                id=f"large-request",
                inputs=[
                    # 10 is the max batch size, so we send a minibatch with
                    # 20 entries
                    RequestInput(
                        name="input-0",
                        shape=[10 * 2, 3],
                        datatype="INT32",
                        data=[n for n in range(10 * 2 * 3)],
                    )
                ],
            ),
            InferenceRequest(
                id=f"regular-request",
                inputs=[
                    RequestInput(
                        name="input-0",
                        shape=[1, 3],
                        datatype="INT32",
                        data=[1000, 1001, 1002],
                    )
                ],
            ),
        ],
    ],
)
async def test_predict(
    requests: List[InferenceRequest],
    adaptive_batcher: AdaptiveBatcher,
    sum_model: MLModel,
):
    responses = await asyncio.gather(
        *[adaptive_batcher.predict(request) for request in requests]
    )

    assert len(requests) == len(responses)
    for req, res in zip(requests, responses):
        assert req.id == res.id

        req_shape = Shape(req.inputs[0].shape)
        res_shape = Shape(res.outputs[0].shape)
        assert req_shape.batch_size == res_shape.batch_size

        expected = await sum_model.predict(req)
        assert res == expected
