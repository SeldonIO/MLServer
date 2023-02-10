import asyncio

from multiprocessing import Queue
from typing import Awaitable, Callable, Dict, Optional, List

from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings
from ..env import Environment

from .model import ParallelModel
from .worker import Worker
from .utils import configure_inference_pool, terminate_queue
from .messages import (
    ModelResponseMessage,
    ModelUpdateMessage,
    ModelUpdateType,
)
from .logging import logger
from .dispatcher import Dispatcher


PredictMethod = Callable[[InferenceRequest], Awaitable[InferenceResponse]]
InferencePoolHook = Callable[[Worker], Awaitable[None]]


class InferencePool:
    """
    The InferencePool class represents a pool of workers where we can run
    inference on.

    Under the hood, it's responsible for managing a pool of multiprocessing
    workers, where the model is loaded.
    This approach lets MLServer work around the GIL to make sure that inference
    can occur in parallel across multiple models or instances of a model.
    """

    def __init__(
        self,
        settings: Settings,
        env: Optional[Environment] = None,
        on_worker_stop: List[InferencePoolHook] = [],
    ):
        configure_inference_pool(settings)

        # TODO: Hook on_worker_stop to "worker unexpectedly died" event
        self._on_worker_stop = on_worker_stop
        self._workers: Dict[int, Worker] = {}
        self._settings = settings
        self._responses: Queue[ModelResponseMessage] = Queue()
        for idx in range(self._settings.parallel_workers):
            # TODO: Set callback to restart worker if it goes down (would
            # `worker.join` help with that?)
            worker = Worker(settings, self._responses, env)
            worker.start()
            self._workers[worker.pid] = worker  # type: ignore

        self._dispatcher = Dispatcher(self._workers, self._responses)
        self._dispatcher.start()

    async def load_model(self, model: MLModel) -> MLModel:
        if not self._should_load_model(model):
            # Skip load if model has disabled parallel workers
            return model

        load_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Load,
            model_settings=model.settings,  # type: ignore
        )
        await self._dispatcher.dispatch_update(load_message)

        return ParallelModel(model, self._dispatcher)

    async def reload_model(self, old_model: MLModel, new_model: MLModel) -> MLModel:
        # The model registries within each worker will take care of reloading
        # the model internally
        return await self.load_model(new_model)

    async def unload_model(self, model: MLModel) -> MLModel:
        if not self._should_load_model(model):
            # Skip unload if model has disabled parallel workers
            return model

        unload_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Unload,
            model_settings=model.settings,  # type: ignore
        )
        await self._dispatcher.dispatch_update(unload_message)

        return ParallelModel(model, self._dispatcher)

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
        await terminate_queue(self._responses)
        self._responses.close()
        await self._dispatcher.stop()
        logger.info("Inference pool shutdown complete")

    async def _close_workers(self):
        # First close down model updates loop
        for pid, worker in self._workers.items():
            await worker.stop()
            worker.join(self._settings.parallel_workers_timeout)
            if worker.exitcode is None:
                worker.kill()
            await asyncio.gather(
                *[callback(worker) for callback in self._on_worker_stop]
            )

        self._workers.clear()
