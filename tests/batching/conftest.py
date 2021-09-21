import pytest
import random

from typing import Callable, Tuple, Awaitable

from mlserver.utils import generate_uuid
from mlserver.types import InferenceRequest, TensorData
from mlserver.model import MLModel
from mlserver.batching.adaptive import AdaptiveBatcher

TestRequestSender = Callable[[], Awaitable[Tuple[str, InferenceRequest]]]


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

        # Generate random data to ensure we catch any out-of-order issues
        request_input = inference_request.inputs[0]
        request_input.data = TensorData(
            __root__=[random.randint(1, 100) for _ in range(3)]
        )
        new_req = InferenceRequest(id=pred_id, inputs=[request_input])
        internal_id, _ = await adaptive_batcher._queue_request(new_req)

        return internal_id, new_req

    return _send_request
