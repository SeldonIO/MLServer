import asyncio
import pytest

from typing import Tuple

from aioprocessing import AioQueue, AioJoinableQueue

from mlserver.settings import ModelSettings, Settings
from mlserver.types import InferenceRequest
from mlserver.utils import generate_uuid
from mlserver.model import MLModel
from mlserver.parallel.pool import InferencePool
from mlserver.parallel.worker import Worker
from mlserver.parallel.utils import terminate_queue, cancel_task
from mlserver.parallel.messages import (
    ModelUpdateMessage,
    ModelUpdateType,
    InferenceRequestMessage,
)


@pytest.fixture
async def pool(settings: Settings, sum_model: MLModel) -> InferencePool:
    pool = InferencePool(settings)
    await pool.load_model(sum_model)
    yield pool

    await pool.close()


@pytest.fixture
async def model_updates() -> AioJoinableQueue:
    q = AioJoinableQueue()
    yield q

    await terminate_queue(q)
    q.close()


@pytest.fixture
async def requests() -> AioQueue:
    q = AioQueue()
    yield q

    await terminate_queue(q)
    q.close()


@pytest.fixture
async def responses() -> AioQueue:
    q = AioQueue()
    yield q

    q.close()


@pytest.fixture
async def worker(
    requests: AioQueue,
    responses: AioQueue,
    model_updates: AioJoinableQueue,
    load_message: ModelUpdateMessage,
) -> Worker:
    worker = Worker(requests, responses, model_updates)

    worker_task = asyncio.create_task(worker.coro_run())

    await model_updates.coro_put(load_message)
    await model_updates.coro_join()

    yield worker

    await worker.close()
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
