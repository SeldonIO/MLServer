import asyncio
import pytest

from multiprocessing import Queue, JoinableQueue
from concurrent.futures import ThreadPoolExecutor

from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest
from mlserver.utils import generate_uuid
from mlserver.model import MLModel
from mlserver.parallel.pool import InferencePool
from mlserver.parallel.worker import Worker
from mlserver.parallel.utils import cancel_task
from mlserver.parallel.messages import (
    ModelUpdateMessage,
    ModelUpdateType,
    InferenceRequestMessage,
)


@pytest.fixture
async def inference_pool(
    inference_pool: InferencePool, sum_model: MLModel
) -> InferencePool:
    await inference_pool.load_model(sum_model)

    yield inference_pool

    print("unloading stuff")
    await inference_pool.unload_model(sum_model)
    print("unloaded things")


@pytest.fixture
async def model_updates() -> JoinableQueue:
    q = JoinableQueue()
    yield q

    q.close()


@pytest.fixture
async def requests() -> Queue:
    q = Queue()
    yield q

    q.close()


@pytest.fixture
async def responses() -> Queue:
    q = Queue()
    yield q

    q.close()


@pytest.fixture
async def worker(
    requests: Queue,
    responses: Queue,
    model_updates: JoinableQueue,
    load_message: ModelUpdateMessage,
) -> Worker:
    loop = asyncio.get_event_loop()
    worker = Worker(requests, responses, model_updates)

    # Simulate the worker running on a different process, but keep it to a
    # thread to simplify debugging
    worker_task = loop.run_in_executor(None, worker.run)

    await worker.send_update(load_message)

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
) -> InferenceRequestMessage:
    return InferenceRequestMessage(
        id=generate_uuid(),
        model_name=sum_model_settings.name,
        model_version=sum_model_settings.parameters.version,
        inference_request=inference_request,
    )
