import asyncio

from concurrent.futures import ProcessPoolExecutor

from .settings import ModelSettings
from .model import MLModel
from .types import InferenceRequest, InferenceResponse


def _mp_load(model_settings: ModelSettings) -> bool:
    """
    This method is meant to run internally in the multiprocessing workers.
    The loading needs to run synchronously, since the initializer argument
    doesn't support coroutines.

    # TODO: Open issue about async initializers
    """
    # NOTE: The global `_mp_model` variable is shared with the `_mp_predict`
    # method.
    # This global variable should only be used within the inference
    # multiprocessing workers.
    global _mp_model

    model_class = model_settings.implementation
    _mp_model = model_class(model_settings)  # type: ignore
    return asyncio.run(_mp_model.load())


def _mp_predict(payload: InferenceRequest) -> InferenceResponse:
    """
    This method is meant to run internally in the multiprocessing workers.
    The prediction needs to run synchronously, since multiprocessing
    doesn't know how to serialise coroutines.
    """
    # NOTE: `_mp_model` is a global variable initialised in the `_mp_load`
    # method.
    # This global variable is only to be used within the inference worker
    # context.
    return asyncio.run(_mp_model.predict(payload))


class ParallelRuntime(MLModel):
    """
    Model proxy responsible of wrapping an existing model runtime and
    "bypassing" some of the calls, so that they get run in a pool of
    multiprocessing workers.

    The interface exposed to the outside world should be equivalent to a
    regular model, so that the multiprocessing is transparent.
    """

    def __init__(self, model: MLModel):
        # TODO: Add custom handlers dynamically
        self._model = model
        self._executor = None

        super().__init__(model._settings)

    def __del__(self):
        if self._executor is not None:
            self._executor.shutdown(wait=True)

    @property
    def ready(self) -> bool:
        return self._model.ready

    @ready.setter
    def ready(self, ready: bool):
        self._model.ready = ready

    async def load(self) -> bool:
        await self._model.load()

        # TODO: Read the number of workers from the model settings
        self._executor = ProcessPoolExecutor(
            initializer=_mp_load, initargs=(self._model._settings,)
        )

        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # What if we serialise payload?
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, _mp_predict, payload)
