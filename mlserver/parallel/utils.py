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
        # force set to True to override the "fork" setting used in pytest
        multiprocessing.set_start_method("spawn", force=True)
    except RuntimeError:
        # TODO: Log warning saying that mp start method couldn't be set
        pass


async def terminate_queue(queue: Queue):
    try:
        # Send sentinel value to terminate queue
        queue.put(END_OF_QUEUE)
    except (ValueError, AssertionError):
        # Most likely, queue is already closed
        return


async def cancel_task(task: Task):
    try:
        task.cancel()
        await task
    except asyncio.CancelledError:
        pass
