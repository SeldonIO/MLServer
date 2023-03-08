import pytest

from mlserver.model import MLModel
from mlserver.parallel.registry import InferencePoolRegistry
from mlserver.types import InferenceRequest
from mlserver.codecs import StringCodec

from ..fixtures import EnvModel


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


async def test_load_model_with_env(
    inference_pool_registry: InferencePoolRegistry,
    env_model_settings: MLModel,
    inference_request: InferenceRequest,
):
    env_model = EnvModel(env_model_settings)

    model = await inference_pool_registry.load_model(env_model)
    response = await model.predict(inference_request)

    assert len(response.outputs) == 1

    # Note: These versions come from the `environment.yml` found in
    # `./tests/testdata/environment.yaml`
    assert response.outputs[0].name == "sklearn_version"
    [sklearn_version] = StringCodec.decode_output(response.outputs[0])
    assert sklearn_version == "1.0.2"

    await inference_pool_registry.unload_model(env_model)
