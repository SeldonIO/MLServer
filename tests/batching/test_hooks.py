import pytest

from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.batching.hooks import load_batching


async def test_batching_predict(
    sum_model: MLModel, inference_request: InferenceRequest
):
    await load_batching(sum_model)
    response = await sum_model.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1


async def test_batching_predict_stream(
    stream_model: MLModel, inference_request: InferenceRequest, caplog
):
    # Force batching to be enabled
    stream_model.settings.max_batch_size = 10
    stream_model.settings.max_batch_time = 0.4
    await load_batching(stream_model)

    stream = stream_model.predict_stream(inference_request)

    assert "not supported for inference streaming" in caplog.text

    responses = [r async for r in stream]
    assert len(response) > 0
    assert isinstance(responses[0], InferenceResponse)
    assert len(response[0].outputs) == 1


@pytest.mark.parametrize(
    "max_batch_size, max_batch_time",
    [
        (0, 10),
        (-1, 10),
        (1, 10),
        (10, 0),
        (10, -1),
        (0, 0),
    ],
)
async def test_load_batching_disabled(
    max_batch_size: int, max_batch_time: float, sum_model: MLModel
):
    sum_model.settings.max_batch_size = max_batch_size
    sum_model.settings.max_batch_time = max_batch_time

    expected = sum_model.predict
    await load_batching(sum_model)

    assert expected == sum_model.predict  # type: ignore
