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


# @pytest.mark.parametrize("method_name", ["generate", "generate_stream"])
# async def test_batching_generate_warning(
#     method_name: str,
#     text_stream_model: MLModel,
#     inference_request: InferenceRequest,
#     caplog,
# ):
#     # Force batching to be enabled
#     text_stream_model.settings.max_batch_size = 10
#     text_stream_model.settings.max_batch_time = 0.4
#     await load_batching(text_stream_model)

#     method = getattr(text_stream_model, method_name)
#     if method_name == "generate_stream":
#         stream = method(inference_request)
#         responses = [r async for r in stream]

#         assert len(responses) > 0
#         assert isinstance(responses[0], InferenceResponse)
#         assert len(responses[0].outputs) == 1
#     else:
#         response = await method(inference_request)

#         assert response is not None
#         assert isinstance(response, InferenceResponse)
#         assert len(response.outputs) == 1

#     assert f"but not required for {method_name} method." in caplog.records[0].message


async def test_batching_predict_stream(
    text_stream_model: MLModel, generate_request: InferenceRequest, caplog
):
    # Force batching to be enabled
    text_stream_model.settings.max_batch_size = 10
    text_stream_model.settings.max_batch_time = 0.4
    await load_batching(text_stream_model)

    async def get_stream_request(request):
        yield request

    stream = text_stream_model.predict_stream(get_stream_request(generate_request))
    responses = [r async for r in stream]

    assert len(responses) > 0
    assert isinstance(responses[0], InferenceResponse)
    assert len(responses[0].outputs) == 1
    assert "not supported for inference streaming" in caplog.records[0].message


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
