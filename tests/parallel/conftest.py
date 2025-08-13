import asyncio
import pytest

from multiprocessing import Queue

from mlserver.settings import Settings, ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver.model import MLModel
from mlserver.env import Environment
from mlserver.parallel.dispatcher import Dispatcher
from mlserver.parallel.model import ModelMethods
from mlserver.parallel.pool import InferencePool, _spawn_worker
from mlserver.parallel.worker import Worker
from mlserver.parallel.utils import configure_inference_pool, cancel_task
from mlserver.parallel.messages import (
    ModelUpdateMessage,
    ModelUpdateType,
    ModelRequestMessage,
)

from ..fixtures import ErrorModel, EnvModel


@pytest.fixture
async def inference_pool(settings: Settings) -> InferencePool:
    pool = InferencePool(settings)
    yield pool
    await pool.close()


@pytest.fixture
async def dispatcher(inference_pool) -> Dispatcher:
    # The InferencePool starts the dispatcher processing loop internally.
    return inference_pool._dispatcher


@pytest.fixture
async def error_model(inference_pool: InferencePool, error_model: MLModel) -> MLModel:
    model = await inference_pool.load_model(error_model)
    yield model
    await inference_pool.unload_model(error_model)


@pytest.fixture
async def load_error_model() -> MLModel:
    error_model_settings = ModelSettings(
        name="foo",
        implementation=ErrorModel,
        parameters=ModelParameters(load_error=True),
    )
    error_model = ErrorModel(error_model_settings)
    yield error_model


@pytest.fixture
def settings(settings: Settings, tmp_path: str) -> Settings:
    # Keep parallelism explicit; tests expect a pool to exist.
    settings.parallel_workers = 2
    settings.environments_dir = str(tmp_path)
    configure_inference_pool(settings)
    return settings


@pytest.fixture
async def responses(settings: Settings) -> Queue:
    # Ensure MP context configured (handled by configure_inference_pool).
    q = Queue()
    yield q
    q.close()


@pytest.fixture
async def worker(
    settings: Settings,
    event_loop: asyncio.AbstractEventLoop,
    responses: Queue,
    load_message: ModelUpdateMessage,
) -> Worker:
    worker = Worker(settings, responses)

    # Simulate a separate process by running the worker loop in a thread.
    # Use coro_run (not run) to avoid extra setup duplication.
    worker_task = event_loop.run_in_executor(
        None, lambda: asyncio.run(worker.coro_run())
    )

    # Load the baseline model into this worker and wait for the ack.
    worker.send_update(load_message)
    responses.get()

    yield worker

    await worker.stop()
    await cancel_task(worker_task)


@pytest.fixture
def load_message(sum_model_settings: ModelSettings) -> ModelUpdateMessage:
    return ModelUpdateMessage(
        update_type=ModelUpdateType.Load, model_settings=sum_model_settings
    )


@pytest.fixture
def unload_message(sum_model_settings: ModelSettings) -> ModelUpdateMessage:
    return ModelUpdateMessage(
        update_type=ModelUpdateType.Unload, model_settings=sum_model_settings
    )


@pytest.fixture
def inference_request_message(
    sum_model_settings: ModelSettings, inference_request: InferenceRequest
) -> ModelRequestMessage:
    # Let the Pydantic model auto-generate `id`; keep args as a list.
    return ModelRequestMessage(
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name=ModelMethods.Predict.value,
        method_args=[inference_request],
    )


@pytest.fixture
def metadata_request_message(sum_model_settings: ModelSettings) -> ModelRequestMessage:
    return ModelRequestMessage(
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name=ModelMethods.Metadata.value,
    )


@pytest.fixture
def custom_request_message(sum_model_settings: ModelSettings) -> ModelRequestMessage:
    # From `SumModel` class in tests/fixtures.py
    return ModelRequestMessage(
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name="my_payload",
        method_kwargs={"payload": [1, 2, 3]},
    )


@pytest.fixture
def env_model_settings(env_tarball: str) -> ModelSettings:
    return ModelSettings(
        name="env-model",
        implementation=EnvModel,
        parameters=ModelParameters(environment_tarball=env_tarball),
    )


@pytest.fixture
def existing_env_model_settings(env_tarball: str, tmp_path) -> ModelSettings:
    from mlserver.env import _extract_env

    env_path = str(tmp_path)
    _extract_env(env_tarball, env_path)
    model_settings = ModelSettings(
        name="exising_env_model",
        implementation=EnvModel,
        parameters=ModelParameters(environment_path=env_path),
    )
    yield model_settings


@pytest.fixture
async def worker_with_env(
    settings: Settings,
    responses: Queue,
    env: Environment,
    env_model_settings: ModelSettings,
):
    # Start a real worker in a separate process for env-dependent tests.
    worker = _spawn_worker(settings, responses, env)

    load_message = ModelUpdateMessage(
        update_type=ModelUpdateType.Load, model_settings=env_model_settings
    )
    worker.send_update(load_message)
    responses.get()

    yield worker

    await worker.stop()


# ---------------------------------------------------------------------
# NEW: helper fixtures for streaming requests (used by streaming tests)
# ---------------------------------------------------------------------


@pytest.fixture
def stream_request_message(sum_model_settings: ModelSettings) -> ModelRequestMessage:
    """
    Build a request message targeting a (mocked) streaming method.
    The tests can patch the model to add `stream_tokens` and then use this.
    """
    return ModelRequestMessage(
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name="stream_tokens",
        method_args=[],
        method_kwargs={},
    )


@pytest.fixture
def stream_error_request_message(
    sum_model_settings: ModelSettings,
) -> ModelRequestMessage:
    """
    Build a request message targeting a (mocked) streaming method that errors.
    """
    return ModelRequestMessage(
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        method_name="stream_tokens_err",
        method_args=[],
        method_kwargs={},
    )
