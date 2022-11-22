import asyncio
import functools

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable


# TODO: this is very similar to `asyncio.to_thread` (python 3.9+),
# so lets use it at some point.
async def run_sync_as_async(fn: Callable, *args, **kwargs) -> Any:
    loop = asyncio.get_running_loop()
    func_call = functools.partial(fn, *args, **kwargs)
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, func_call)


def run_async_as_sync(func, *args, **kwargs):
    def thread_func(*args, **kwargs):
        # always create new loop as the thread is clean
        # and doesn't run any loop
        loop = asyncio.new_event_loop()
        try:
            inner_func = args[0]
            args = args[1:]
            res = loop.run_until_complete(inner_func(*args, **kwargs))
            return res
        finally:
            loop.close()

    # Run the func in separate thread loop
    # in order to avoid re-entrancy of current event loop
    with ThreadPoolExecutor(max_workers=1) as executor:
        if not args:
            args = tuple()
        # the function that should be called is always first argument
        args = (func,) + args
        fut = executor.submit(thread_func, *args, **kwargs)
        return fut.result()
