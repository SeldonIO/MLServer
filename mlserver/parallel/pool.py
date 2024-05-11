import asyncio

from contextlib import nullcontext
from multiprocessing import Queue
from typing import Awaitable, Callable, Dict, Optional, List, Iterable

from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings, ModelSettings
from ..env import Environment

from .model import ParallelModel
from .worker import Worker
from .logging import logger
from .utils import configure_inference_pool, terminate_queue
from .messages import (
    ModelResponseMessage,
    ModelUpdateMessage,
    ModelUpdateType,
)
from .dispatcher import Dispatcher


PredictMethod = Callable[[InferenceRequest], Awaitable[InferenceResponse]]
InferencePoolHook = Callable[[Worker], Awaitable[None]]


def _spawn_worker(settings: Settings, responses: Queue, env: Optional[Environment]):
    with env or nullcontext():
        worker = Worker(settings, responses, env)
        worker.start()

    return worker


class WorkerRegistry:
    """
    Simple registry to keep track of which models have been loaded.
    This can be used to re-load all models when a worker stops unexpectedly.
    """

    def __init__(self) -> None:
        self._models: Dict[str, ModelSettings] = {}

    def _key(self, model_settings: ModelSettings) -> str:
        return f"{model_settings.name}-{model_settings.version}"

    def add(self, model_settings: ModelSettings):
        model_key = self._key(model_settings)
        self._models[model_key] = model_settings

    def remove(self, model_settings: ModelSettings):
        model_key = self._key(model_settings)
        if model_key in self._models:
            del self._models[model_key]

    def __len__(self) -> int:
        return len(self._models)

    @property
    def models(self) -> Iterable[ModelSettings]:
        return self._models.values()


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
        for _ in range(self._settings.parallel_workers):
            worker = _spawn_worker(self._settings, self._responses, self._env)
            self._workers[worker.pid] = worker  # type: ignore

        self._dispatcher = Dispatcher(self._workers, self._responses)
        self._dispatcher.start()

    @property
    def env_hash(self) -> Optional[str]:
        if not self._env:
            return None

        return self._env.env_hash

    @property
    def name(self) -> str:
        if self.env_hash:
            return f"inference pool with hash '{self.env_hash}'"

        return "default inference pool"

    async def on_worker_stop(self, pid: int, exit_code: int):
        if pid not in self._workers:
            # If this worker didn't belong to this pool, ignore
            return

        worker = self._workers[pid]
        logger.warning(
            f"Worker with PID {worker.pid} on {self.name} stopped "
            f"unexpectedly with exit code {exit_code}. "
            "Triggering worker restart..."
        )
        self._dispatcher.on_worker_stop(worker, exit_code)
        if pid in self._workers:
            # NOTE: worker may be removed by dispatcher
            del self._workers[pid]

        # Call attached on_worker_stop hooks
        await asyncio.gather(*[callback(worker) for callback in self._on_worker_stop])

        # Start a new worker
        await self._start_worker()

    async def _start_worker(self) -> Worker:
        worker = _spawn_worker(self._settings, self._responses, self._env)
        logger.info(f"Starting new worker with PID {worker.pid} on {self.name}...")

        # Add to dispatcher so that it can receive load requests and reload all
        # models
        self._workers[worker.pid] = worker  # type: ignore
        await self._dispatcher.on_worker_start(worker)

        await asyncio.gather(
            *[
                self._dispatcher.dispatch_update_to_worker(
                    worker,
                    ModelUpdateMessage(
                        update_type=ModelUpdateType.Load,
                        model_settings=model_settings,  # type: ignore
                    ),
                )
                for model_settings in self._worker_registry.models
            ]
        )

        # Once all models are loaded, we notify the dispatcher to reload all
        # models
        self._dispatcher.on_worker_ready(worker)

        logger.info(f"New worker with PID {worker.pid} on {self.name} is now ready.")
        return worker

    async def load_model(self, model: MLModel) -> MLModel:
        load_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Load,
            model_settings=model.settings,  # type: ignore
        )
        await self._dispatcher.dispatch_update(load_message)

        self._worker_registry.add(model.settings)
        return ParallelModel(model, self._dispatcher)

    async def reload_model(self, old_model: MLModel, new_model: MLModel) -> MLModel:
        # The model registries within each worker will take care of reloading
        # the model internally
        self._worker_registry.remove(old_model.settings)
        self._worker_registry.add(new_model.settings)
        return await self.load_model(new_model)

    async def unload_model(self, model: MLModel) -> MLModel:
        unload_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Unload,
            model_settings=model.settings,  # type: ignore
        )
        await self._dispatcher.dispatch_update(unload_message)

        self._worker_registry.remove(model.settings)
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
