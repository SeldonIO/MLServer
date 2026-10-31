import asyncio
import pytest

from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.batching.hooks import load_batching

from ..fixtures import SumModel


@pytest.mark.parametrize("cancelled_index", [None, 0, 1])
@pytest.mark.parametrize("fail_prediction", [False, True])
async def test_batching_cancelled_request(
    sum_model_settings, cancelled_index, fail_prediction
):
    started = asyncio.Event()
    release = asyncio.Event()
    model_error = RuntimeError("prediction failed")
    batch_shapes = []

    class GatedSumModel(SumModel):
        async def predict(self, payload):
            batch_shapes.append(payload.inputs[0].shape)
            started.set()
            await release.wait()
            if fail_prediction:
                raise model_error
            return await super().predict(payload)

    sum_model_settings.max_batch_size = 2
    sum_model_settings.max_batch_time = 0.01
    model = await load_batching(GatedSumModel(sum_model_settings))
    requests = [
        InferenceRequest(
            id=f"request-{idx}",
            inputs=[
                {
                    "name": "input-0",
                    "shape": [1, 3],
                    "datatype": "INT32",
                    "data": [idx, idx + 1, idx + 2],
                }
            ],
        )
        for idx in range(2)
    ]
    tasks = [asyncio.create_task(model.predict(request)) for request in requests]
    loop = asyncio.get_running_loop()
    callback_errors = []
    previous_handler = loop.get_exception_handler()
    loop.set_exception_handler(lambda loop, context: callback_errors.append(context))
    try:
        await asyncio.wait_for(started.wait(), timeout=1)
        assert batch_shapes == [[2, 3]]
        if cancelled_index is not None:
            tasks[cancelled_index].cancel()
            with pytest.raises(asyncio.CancelledError):
                await tasks[cancelled_index]

        release.set()
        active_indices = [idx for idx in range(2) if idx != cancelled_index]
        responses = await asyncio.wait_for(
            asyncio.gather(
                *(tasks[idx] for idx in active_indices), return_exceptions=True
            ),
            timeout=1,
        )
        for idx, response in zip(active_indices, responses):
            if fail_prediction:
                assert response is model_error
            else:
                assert response.id == requests[idx].id
                assert response.outputs[0].shape == [1, 1]
                assert response.outputs[0].data.root == [3 * idx + 3]
        assert not callback_errors

        # The same batcher must remain usable after cancellation or a model error.
        fail_prediction = False
        following = await asyncio.wait_for(model.predict(requests[0]), timeout=1)
        assert following.id == requests[0].id
        assert following.outputs[0].data.root == [3]
        assert not callback_errors
    finally:
        release.set()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        loop.set_exception_handler(previous_handler)


async def test_batching_predict(
    sum_model: MLModel, inference_request: InferenceRequest
):
    await load_batching(sum_model)
    response = await sum_model.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1


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
