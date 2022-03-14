from aioprocessing import AioQueue, AioConnection
from aioprocessing.process import Process

from ..registry import MultiModelRegistry


class WorkerProcess(Process):
    def __init__(
        self, requests: AioQueue, responses: AioQueue, model_updates: AioConnection
    ):
        super().__init__()
        self._requests = requests
        self._responses = responses
        self._model_updates = model_updates

        self._model_registry = MultiModelRegistry()
        self._active = True
        self._future_update = None

    async def run(self):
        # NOTE: The `_process_model_updates` function will take care of
        # chaining itself to the next (future) model update. Therefore it will
        # always be running.
        self._process_model_updates()
        while self._active:
            request = await self._requests.coro_get()

            # TODO: Extract the inferencerequest and the model name + version
            # from message
            name, version, payload = request

            model = await self._model_registry.get_model(name, version)
            inference_response = await model.predict(payload)

            await self._responses.coro_put(inference_response)

    async def _process_model_updates(self):
        while not self._model_updates.empty():
            model_update = await self._model_updates.coro_get()

            # TODO: Check type of update, which could be load or unload
            pass

        # Chain next update
        self._future_update = self._model_updates.coro_get()
        self._future_update.add_done_callback(
            lambda: asyncio.run(self._process_model_updates)
        )

        return self._future_update
