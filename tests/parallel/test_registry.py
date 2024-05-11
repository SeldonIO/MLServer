import pytest
import os
import asyncio

from mlserver.env import Environment, compute_hash
from mlserver.model import MLModel
from mlserver.settings import Settings, ModelSettings
from mlserver.types import InferenceRequest
from mlserver.codecs import StringCodec
from mlserver.parallel.errors import EnvironmentNotFound
from mlserver.parallel.registry import (
    InferencePoolRegistry,
    _set_environment_hash,
    _get_environment_hash,
    ENV_HASH_ATTR,
)

from ..fixtures import EnvModel


@pytest.fixture
async def env_model(
    inference_pool_registry: InferencePoolRegistry, env_model_settings: ModelSettings
) -> MLModel:
    env_model = EnvModel(env_model_settings)
    model = await inference_pool_registry.load_model(env_model)

    yield model

    await inference_pool_registry.unload_model(model)


def test_set_environment_hash(sum_model: MLModel):
    env_hash = "0e46fce1decb7a89a8b91c71d8b6975630a17224d4f00094e02e1a732f8e95f3"
    _set_environment_hash(sum_model, env_hash)

    assert hasattr(sum_model, ENV_HASH_ATTR)
    assert getattr(sum_model, ENV_HASH_ATTR) == env_hash


@pytest.mark.parametrize(
    "env_hash",
    ["0e46fce1decb7a89a8b91c71d8b6975630a17224d4f00094e02e1a732f8e95f3", None],
)
def test_get_environment_hash(sum_model: MLModel, env_hash: str):
    if env_hash:
        _set_environment_hash(sum_model, env_hash)

    assert _get_environment_hash(sum_model) == env_hash


async def test_default_pool(
    inference_pool_registry: InferencePoolRegistry, settings: Settings
):
    assert inference_pool_registry._default_pool is not None

    worker_count = len(inference_pool_registry._default_pool._workers)
    assert worker_count == settings.parallel_workers


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
    env_model: MLModel,
    inference_request: InferenceRequest,
):
    response = await env_model.predict(inference_request)

    assert len(response.outputs) == 1

    # Note: These versions come from the `environment.yml` found in
    # `./tests/testdata/environment.yaml`
    assert response.outputs[0].name == "sklearn_version"
    [sklearn_version] = StringCodec.decode_output(response.outputs[0])
    assert sklearn_version == "1.0.2"


async def test_load_creates_or_reuses_pool(
    inference_pool_registry: InferencePoolRegistry,
    env_model_settings: MLModel,
):
    # Create new pool
    assert len(inference_pool_registry._pools) == 0
    env_model = EnvModel(env_model_settings)
    await inference_pool_registry.load_model(env_model)
    assert len(inference_pool_registry._pools) == 1

    # Reuse pool
    env_model_settings.name = "foo"
    new_model = EnvModel(env_model_settings)
    await inference_pool_registry.load_model(new_model)
    assert len(inference_pool_registry._pools) == 1


async def test_load_reuses_env_folder(
    inference_pool_registry: InferencePoolRegistry,
    env_model_settings: ModelSettings,
    env_tarball: str,
):
    env_model_settings.name = "foo"
    new_model = EnvModel(env_model_settings)

    # Make sure there's already existing env
    env_hash = await compute_hash(env_tarball)
    env_path = inference_pool_registry._get_env_path(env_hash)
    await Environment.from_tarball(env_tarball, env_path, env_hash)

    await inference_pool_registry.load_model(new_model)


async def test_reload_model_with_env(
    inference_pool_registry: InferencePoolRegistry,
    env_model: MLModel,
    env_model_settings: ModelSettings,
):
    env_model_settings.parameters.version = "v2.0"
    new_model = EnvModel(env_model_settings)

    assert len(inference_pool_registry._pools) == 1
    await inference_pool_registry.reload_model(env_model, new_model)

    assert len(inference_pool_registry._pools) == 1


async def test_unload_model_removes_pool_if_empty(
    inference_pool_registry: InferencePoolRegistry,
    env_model_settings: MLModel,
):
    env_model = EnvModel(env_model_settings)
    assert len(inference_pool_registry._pools) == 0

    model = await inference_pool_registry.load_model(env_model)
    assert len(inference_pool_registry._pools) == 1

    await inference_pool_registry.unload_model(model)

    env_hash = _get_environment_hash(model)
    env_path = inference_pool_registry._get_env_path(env_hash)
    assert len(inference_pool_registry._pools) == 0
    assert not os.path.isdir(env_path)


async def test_invalid_env_hash(
    inference_pool_registry: InferencePoolRegistry, sum_model: MLModel
):
    _set_environment_hash(sum_model, "foo")
    with pytest.raises(EnvironmentNotFound):
        await inference_pool_registry._find(sum_model)


async def test_worker_stop(
    settings: Settings,
    inference_pool_registry: InferencePoolRegistry,
    sum_model: MLModel,
    inference_request: InferenceRequest,
    caplog,
):
    # Pick random worker and kill it
    default_pool = inference_pool_registry._default_pool
    workers = list(default_pool._workers.values())
    stopped_worker = workers[0]
    stopped_worker.kill()

    # Give some time for worker to come up
    await asyncio.sleep(5)

    # Ensure SIGCHD signal was handled
    assert f"with PID {stopped_worker.pid}" in caplog.text

    # Cycle through every worker
    assert len(default_pool._workers) == settings.parallel_workers
    for _ in range(settings.parallel_workers + 2):
        inference_response = await sum_model.predict(inference_request)
        assert len(inference_response.outputs) > 0
