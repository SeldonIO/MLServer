from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.batching.listeners import load_batching


async def test_batching_predict(
    sum_model: MLModel, inference_request: InferenceRequest
):
    await load_batching(sum_model)
    response = await sum_model.predict(inference_request)

    assert response is not None
    assert isinstance(response, InferenceResponse)
    assert len(response.outputs) == 1
