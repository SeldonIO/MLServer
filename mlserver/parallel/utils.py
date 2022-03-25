import asyncio
import multiprocessing

from asyncio import Task
from aioprocessing import AioQueue
from typing import Callable, Awaitable

from mlserver.settings import Settings

END_OF_QUEUE = None


def configure_inference_pool(settings: Settings):
    # Set MP method
    multiprocessing.set_start_method("spawn")


async def terminate_queue(queue: AioQueue):
    # Send sentinel value to terminate queue
    await queue.coro_put(END_OF_QUEUE)


async def cancel_task(task: Task):
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


def syncify(async_f: Callable[[], Awaitable[None]]):
    def sync_f(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(async_f(*args, **kwargs))

    return sync_f
