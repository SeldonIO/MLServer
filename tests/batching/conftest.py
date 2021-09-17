import pytest

from typing import Callable, Awaitable

from mlserver.utils import generate_uuid
from mlserver.types import InferenceRequest
from mlserver.model import MLModel
from mlserver.batching.adaptive import AdaptiveBatcher

TestRequestSender = Callable[[], Awaitable[InferenceRequest]]


@pytest.fixture
def adaptive_batcher(sum_model: MLModel) -> AdaptiveBatcher:
    return AdaptiveBatcher(sum_model)


@pytest.fixture
def send_request(
    adaptive_batcher: AdaptiveBatcher, inference_request: InferenceRequest
) -> TestRequestSender:
    async def _send_request():
        # Change the UUID so that it's a new one
        pred_id = generate_uuid()
        new_req = InferenceRequest(id=pred_id, inputs=inference_request.inputs)
        await adaptive_batcher._queue_request(new_req)

        return new_req

    return _send_request
