import asyncio

from typing import Callable, Awaitable


def syncify(async_f: Callable[[], Awaitable[None]]):
    def sync_f(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(async_f(*args, **kwargs))

    return sync_f
