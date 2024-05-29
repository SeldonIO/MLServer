import os
import pytest
import random

from typing import Callable, Tuple, Awaitable

from mlserver.utils import generate_uuid
from mlserver.types import InferenceRequest, TensorData
from mlserver.model import MLModel
from mlserver.context import model_context
from mlserver.batching.adaptive import AdaptiveBatcher
from mlserver.settings import ModelSettings

from ..conftest import TESTDATA_PATH

TestRequestSender = Callable[[], Awaitable[Tuple[str, InferenceRequest]]]


@pytest.fixture(autouse=True)
def sum_model_context(sum_model_settings: ModelSettings) -> ModelSettings:
    with model_context(sum_model_settings):
        yield sum_model_settings


@pytest.fixture(params=["inference-request.json", "inference-request-with-output.json"])
def inference_request(request) -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, request.param)
    return InferenceRequest.parse_file(payload_path)


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
        request_input.data = TensorData(root=[random.randint(1, 100) for _ in range(3)])
        new_req = InferenceRequest(id=pred_id, inputs=[request_input])
        internal_id, _ = await adaptive_batcher._queue_request(new_req)

        return internal_id, new_req

    return _send_request
