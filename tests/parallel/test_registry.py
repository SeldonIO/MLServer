import pytest

from mlserver.model import MLModel
from mlserver.parallel.registry import InferencePoolRegistry
from mlserver.types import InferenceRequest


async def test_load_model(
    inference_pool_registry: InferencePoolRegistry,
    sum_model: MLModel,
    inference_request: InferenceRequest,
):
    sum_model.settings.name = "foo"
    model = await inference_pool_registry.load_model(sum_model)
    inference_response = await model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model.settings.name
    assert len(inference_response.outputs) == 1

    await inference_pool_registry.unload_model(sum_model)
