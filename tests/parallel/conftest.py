import asyncio
import pytest

from typing import Tuple

from aioprocessing import AioQueue, AioJoinableQueue
from mlserver.settings import ModelSettings

from mlserver.parallel.worker import WorkerProcess
from mlserver.parallel.utils import terminate_queue, cancel_task
from mlserver.parallel.messages import ModelUpdateMessage, ModelUpdateType


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
async def worker_process(
    requests: AioQueue, model_updates: AioJoinableQueue
) -> WorkerProcess:
    responses = AioQueue()
    worker = WorkerProcess(requests, responses, model_updates)

    worker_task = asyncio.create_task(worker.run())

    yield worker

    await worker.close()
    await cancel_task(worker_task)


@pytest.fixture
def load_message(sum_model_settings: ModelSettings) -> ModelUpdateMessage:
    return ModelUpdateMessage(
        update_type=ModelUpdateType.Load, model_settings=sum_model_settings
    )
