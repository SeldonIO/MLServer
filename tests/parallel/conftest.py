import asyncio
import pytest

from asyncio.exceptions import CancelledError
from typing import Tuple

from aioprocessing import AioQueue, AioJoinableQueue
from mlserver.settings import ModelSettings

from mlserver.parallel.worker import WorkerProcess
from mlserver.parallel.messages import ModelUpdateMessage, ModelUpdateType


@pytest.fixture
def model_updates() -> AioJoinableQueue:
    return AioJoinableQueue()


@pytest.fixture
async def worker_process(model_updates: AioJoinableQueue) -> WorkerProcess:
    requests = AioQueue()
    responses = AioQueue()
    worker = WorkerProcess(requests, responses, model_updates)

    worker_task = asyncio.create_task(worker.run())

    yield worker

    await worker.close()
    requests.close()
    worker_task.cancel()
    try:
        print("awaiting worker task")
        await worker_task
    except CancelledError:
        pass
    print("awaited worker task")


@pytest.fixture
def load_message(sum_model_settings: ModelSettings) -> ModelUpdateMessage:
    return ModelUpdateMessage(
        update_type=ModelUpdateType.Load, model_settings=sum_model_settings
    )
