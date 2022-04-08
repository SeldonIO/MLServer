import asyncio
import multiprocessing

from asyncio import Task
from multiprocessing import Queue

from mlserver.settings import Settings

END_OF_QUEUE = None


def configure_inference_pool(settings: Settings):
    if not settings.parallel_workers:
        return

    # Set MP method
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        # TODO: Log warning saying that mp start method couldn't be set
        pass


async def terminate_queue(queue: Queue):
    # Send sentinel value to terminate queue
    queue.put(END_OF_QUEUE)


async def cancel_task(task: Task):
    try:
        task.cancel()
        await task
    except asyncio.CancelledError:
        pass
