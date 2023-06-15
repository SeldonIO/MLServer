import asyncio

from multiprocessing import Queue
from typing import Awaitable, Callable, Dict, Optional, List

from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings, ModelSettings
from ..env import Environment

from .model import ParallelModel
from .worker import Worker
from .utils import configure_inference_pool, terminate_queue
from .messages import (
    ModelResponseMessage,
    ModelUpdateMessage,
    ModelUpdateType,
)
from .dispatcher import Dispatcher


PredictMethod = Callable[[InferenceRequest], Awaitable[InferenceResponse]]
InferencePoolHook = Callable[[Worker], Awaitable[None]]


class WorkerRegistry:
    """
    Simple registry to keep track of which models have been loaded.
    This can be used to re-load all models when a worker stops unexpectedly.
    """

    def __init__(self):
        self._models: Dict[str, ModelSettings] = {}

    def _key(self, model_settings: ModelSettings) -> str:
        return f"{model_settings.name}-{model_settings.version}"

    def on_model_load(self, model_settings: ModelSettings):
        model_key = self._key(model_settings)
        self._models[model_key] = model_settings

    def on_model_reload(
        self, old_model_settings: ModelSettings, new_model_settings: ModelSettings
    ):
        self.on_model_unload(old_model_settings)
        self.on_model_load(new_model_settings)

    def on_model_unload(self, model_settings: ModelSettings):
        model_key = self._key(model_settings)
        if model_key in self._models:
            del self._models[model_key]

    def __len__(self) -> int:
        return len(self._models)


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

        self._on_worker_stop = on_worker_stop
        self._env = env
        self._workers: Dict[int, Worker] = {}
        self._worker_registry = WorkerRegistry()
        self._settings = settings
        self._responses: Queue[ModelResponseMessage] = Queue()
        for idx in range(self._settings.parallel_workers):
            worker = Worker(self._settings, self._responses, self._env)
            worker.start()
            self._workers[worker.pid] = worker  # type: ignore

        self._dispatcher = Dispatcher(self._workers, self._responses)
        self._dispatcher.start()

    @property
    def env_hash(self) -> Optional[str]:
        if not self._env:
            return None

        return self._env.env_hash

    def on_worker_stop(self, pid: int, exit_code: int):
        if pid not in self._workers:
            # If this worker didn't belong to this pool, ignore
            return

        # TODO: Call downstream _on_worker_stop hooks
        worker = self._workers[pid]
        self._dispatcher.on_worker_stop(worker, exit_code)
        if pid in self._workers:
            # NOTE: worker may be removed by dispatcher
            del self._workers[pid]

        #  worker = Worker(self._settings, self._responses, self._env)
        #  worker.start()

    async def load_model(self, model: MLModel) -> MLModel:
        load_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Load,
            model_settings=model.settings,  # type: ignore
        )
        await self._dispatcher.dispatch_update(load_message)

        self._worker_registry.on_model_load(model.settings)
        return ParallelModel(model, self._dispatcher)

    async def reload_model(self, old_model: MLModel, new_model: MLModel) -> MLModel:
        # The model registries within each worker will take care of reloading
        # the model internally
        self._worker_registry.on_model_reload(old_model.settings, new_model.settings)
        return await self.load_model(new_model)

    async def unload_model(self, model: MLModel) -> MLModel:
        unload_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Unload,
            model_settings=model.settings,  # type: ignore
        )
        await self._dispatcher.dispatch_update(unload_message)

        self._worker_registry.on_model_unload(model.settings)
        return ParallelModel(model, self._dispatcher)

    def empty(self) -> bool:
        return len(self._worker_registry) == 0

    async def close(self):
        await self._close_workers()
        await terminate_queue(self._responses)
        self._responses.close()
        await self._dispatcher.stop()

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
