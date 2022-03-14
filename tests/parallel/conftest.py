import pytest
import asyncio

from aioprocessing import AioQueue, AioPipe

from mlserver.parallel.worker import WorkerProcess


@pytest.fixture
async def worker_process() -> WorkerProcess:
    requests = AioQueue()
    responses = AioQueue()
    model_updates, _ = AioPipe()
    worker = WorkerProcess(requests, responses, model_updates)

    worker_coro = worker.run()

    yield worker

    worker._active = False
    await worker_coro
