import asyncio
import concurrent.futures


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
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        if not args:
            args = tuple()
        # the function that should be called is always first argument
        args = (func,) + args
        fut = executor.submit(thread_func, *args, **kwargs)
        return fut.result()
