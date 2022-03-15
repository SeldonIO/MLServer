import asyncio

from functools import partial
from aioprocessing import AioQueue, AioJoinableQueue
from aioprocessing.process import Process
from asyncio.exceptions import CancelledError
from typing import Awaitable

from ..registry import MultiModelRegistry

from .messages import ModelUpdateType, ModelUpdateMessage
from .utils import syncify


class WorkerProcess(Process):
    def __init__(
        self, requests: AioQueue, responses: AioQueue, model_updates: AioJoinableQueue
    ):
        super().__init__()
        self._requests = requests
        self._responses = responses
        self._model_updates = model_updates

        self._model_registry = MultiModelRegistry()
        self._active = True
        self._wakeup_task = None

    async def run(self):
        # NOTE: The `_process_model_updates` function will take care of
        # chaining itself to the next (future) model update. Therefore it will
        # always be running.
        await self._process_model_updates()
        while self._active:
            print(f"active is {self._active}")
            request = await self._requests.coro_get(timeout=1)
            print(f"hello")

            #  # TODO: Extract the inferencerequest and the model name + version
            #  # from message
            #  name, version, payload = request

            #  model = await self._model_registry.get_model(name, version)
            #  inference_response = await model.predict(payload)

            #  await self._responses.coro_put(inference_response)

        print("out of run")

    async def _process_model_updates(self):
        while not self._model_updates.empty():
            update = await self._model_updates.coro_get()
            await self._process_model_update(update)
            self._model_updates.task_done()

        # Chain next (future) update once we're done processing the queue
        #  self._wakeup_task = self._model_updates.coro_get()
        #  self._wakeup_task.add_done_callback(self._wakeup_model_updates_loop)

        return self._wakeup_task

    @syncify
    async def _wakeup_model_updates_loop(self, coro_get: Awaitable[ModelUpdateMessage]):
        """
        Helper to 'wake up' the model updates processing loop.
        This method will get called whenever there's a new update to be
        processed, and will re-start the update process loop.

        Note that, due to the limitations of `add_done_callback`, this method
        must be synchronous (hence the `syncify` decorator).
        """
        # Process the `.coro_get()` task that was used to get pinged whenever a
        # new message is available.
        try:
            latest_update = await coro_get
        except CancelledError:
            # In the case where the `_wakeup_task` gets canceled (e.g. when
            # closing the worker), the output of the `coro_get` task will be an
            # exception.
            return

        await self._process_model_update(latest_update)
        self._model_updates.task_done()

        await self._process_model_updates()

    async def _process_model_update(self, update: ModelUpdateMessage):
        model_settings = update.model_settings
        if update.update_type == ModelUpdateType.Load:
            await self._model_registry.load(model_settings)
        elif update.update_type == ModelUpdateType.Unload:
            await self._model_updates.unload(model_settings.name)
        else:
            # TODO: Raise warning about unknown model update
            pass

    async def close(self):
        # TODO: Unload all models
        self._active = False
        if self._wakeup_task is not None:
            # Cancel task
            self._wakeup_task.cancel()
            try:
                print("awaiting cancelled wakeup task - do we need to?")
                await self._wakeup_task
            except CancelledError:
                pass

            print("awaited cancelled wakeup task")
            self._wakeup_task = None
