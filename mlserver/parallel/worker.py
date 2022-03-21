import asyncio

from functools import partial
from aioprocessing import AioQueue, AioJoinableQueue
from aioprocessing.process import Process
from asyncio.exceptions import CancelledError
from typing import Awaitable

from ..registry import MultiModelRegistry

from .messages import ModelUpdateType, ModelUpdateMessage
from .utils import syncify, END_OF_QUEUE, cancel_task


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
            request = await self._requests.coro_get()
            if request is END_OF_QUEUE:
                # TODO: Log info message saying that we are exiting the loop
                # If requests queue gets terminated, detect the sentinel value
                # and stop loop
                return

            # TODO: Where should we check if the model exists? Should that
            # happen in the parent process?
            model = await self._model_registry.get_model(
                request.model_name, request.model_version
            )
            inference_response = await model.predict(request.inference_request)

            await self._responses.coro_put(inference_response)

            await self._responses.coro_put(inference_response)

    async def _process_model_updates(self):
        while not self._model_updates.empty():
            update = await self._model_updates.coro_get()
            await self._process_model_update(update)
            self._model_updates.task_done()

        # Chain next (future) update once we're done processing the queue
        self._wakeup_task = self._model_updates.coro_get()
        self._wakeup_task.add_done_callback(self._wakeup_model_updates_loop)

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
            # If the queue gets terminated, detect the "sentinel value" and
            # stop reading
            if latest_update is END_OF_QUEUE:
                return
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
            await self._model_registry.unload(model_settings.name)
        else:
            # TODO: Raise warning about unknown model update
            pass

    async def close(self):
        # TODO: Unload all models
        self._active = False
        if self._wakeup_task is not None:
            # Cancel task
            await cancel_task(self._wakeup_task)
            self._wakeup_task = None
