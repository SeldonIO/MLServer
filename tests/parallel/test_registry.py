from mlserver.model import MLModel
from mlserver.parallel.registry import PoolRegistry
from mlserver.types import InferenceRequest


def test_load_model(
    pool_registry: PoolRegistry,
    sum_model: MLModel,
    inference_request: InferenceRequest,
):
    model = await pool_registry.load_model(sum_model)
    inference_response = await model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model.settings.name
    assert len(inference_response.outputs) == 1
