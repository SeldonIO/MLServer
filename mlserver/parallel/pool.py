import asyncio

from multiprocessing import Queue
from functools import wraps
from typing import Any, Coroutine, Callable, Dict

from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings, ModelSettings
from ..utils import get_wrapped_method

from .errors import InvalidParallelMethod
from .worker import Worker
from .utils import configure_inference_pool
from .messages import (
    InferenceResponseMessage,
    ModelUpdateMessage,
    ModelUpdateType,
)
from .logging import logger
from .dispatcher import Dispatcher


PredictMethod = Callable[[InferenceRequest], Coroutine[Any, Any, InferenceResponse]]

_InferencePoolAttr = "__inference_pool__"


class InferencePool:
    """
    The InferencePool class represents a pool of workers where we can run
    inference on.

    Under the hood, it's responsible for managing a pool of multiprocessing
    workers, where the model is loaded.
    This approach lets MLServer work around the GIL to make sure that inference
    can occur in parallel across multiple models or instances of a model.
    """

    def __init__(self, settings: Settings):
        configure_inference_pool(settings)

        self._workers: Dict[int, Worker] = {}
        self._settings = settings
        responses: Queue[InferenceResponseMessage] = Queue()
        for idx in range(self._settings.parallel_workers):
            # TODO: Set callback to restart worker if it goes down (would
            # `worker.join` help with that?)
            worker = Worker(responses)
            worker.start()
            self._workers[worker.pid] = worker  # type: ignore

        self._dispatcher = Dispatcher(self._workers, responses)
        self._dispatcher.start()

    async def predict(
        self, model_settings: ModelSettings, inference_request: InferenceRequest
    ) -> InferenceResponse:
        return await self._dispatcher.predict(model_settings, inference_request)

    def parallel(self, f: PredictMethod):
        """
        Decorator to attach to model's methods so that they run in parallel.
        By default, this will get attached to every model's "inference" method.

        NOTE: At the moment, this method only works with `predict()`.
        """
        # TODO: Extend to multiple methods
        @wraps(f)
        async def _inner(payload: InferenceRequest) -> InferenceResponse:
            wrapped_f = get_wrapped_method(f)
            if not hasattr(wrapped_f, "__self__"):
                raise InvalidParallelMethod(
                    wrapped_f.__name__, reason="method is not bound"
                )

            model = getattr(wrapped_f, "__self__")

            return await self.predict(model.settings, payload)

        return _inner

    async def load_model(self, model: MLModel):
        if not self._should_load_model(model):
            # Skip load if model has disabled parallel workers
            return

        load_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Load, model_settings=model.settings
        )
        await asyncio.gather(
            *[worker.send_update(load_message) for worker in self._workers.values()]
        )

        # Decorate predict method
        setattr(model, "predict", self.parallel(model.predict))

    async def reload_model(self, old_model: MLModel, new_model: MLModel):
        # The model registries within each worker will take care of reloading
        # the model internally
        await self.load_model(new_model)

    async def unload_model(self, model: MLModel):
        if not self._should_load_model(model):
            # Skip unload if model has disabled parallel workers
            return

        unload_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Unload, model_settings=model.settings
        )
        await asyncio.gather(
            *[worker.send_update(unload_message) for worker in self._workers.values()]
        )

    def _should_load_model(self, model: MLModel):
        if model.settings.parallel_workers is not None:
            logger.warning(
                "DEPRECATED!! The `parallel_workers` setting at the model-level "
                "has now been deprecated and moved "
                "to the top-level server "
                "settings. "
                "This field will be removed in MLServer 1.2.0. "
                "To access the new field, you can either update the "
                "`settings.json` file, or update the `MLSERVER_PARALLEL_WORKERS` "
                "environment variable. "
                f"The current value of the server-level's `parallel_workers` field is "
                f"'{self._settings.parallel_workers}'."
            )

            # NOTE: This is a remnant from the previous architecture for parallel
            # workers, where each worker had its own pool.
            # For backwards compatibility, we will respect when a model disables
            # parallel inference.
            if model.settings.parallel_workers <= 0:
                return False

        if not self._settings.parallel_workers:
            return False

        return True

    async def close(self):
        logger.info("Waiting for inference pool shutdown")
        await self._close_workers()
        await self._dispatcher.stop()
        logger.info("Inference pool shutdown complete")

    async def _close_workers(self):
        # First close down model updates loop
        for pid, worker in self._workers.items():
            await worker.stop()
            worker.join()

        self._workers.clear()
