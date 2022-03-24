import asyncio

from asyncio import Future
from aioprocessing import AioQueue, AioJoinableQueue
from functools import wraps
from typing import Awaitable, Any, Dict, Coroutine, Callable, Optional

from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings, ModelSettings
from ..utils import get_wrapped_method, generate_uuid

from .worker import Worker
from .utils import syncify, END_OF_QUEUE, terminate_queue, cancel_task
from .messages import (
    InferenceRequestMessage,
    InferenceResponseMessage,
    ModelUpdateMessage,
    ModelUpdateType,
)

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
        # TODO: Read number of workers from settings
        parallel_workers = 4
        self._workers = {}
        self._requests = AioQueue()
        self._responses = AioQueue()
        self._async_responses: Dict[str, Future[InferenceResponse]] = {}
        for idx in range(parallel_workers):
            # TODO: Set callback to restart worker if it goes down (would
            # `worker.join` help with that?)
            model_updates = AioJoinableQueue()
            worker = Worker(self._requests, self._responses, model_updates)
            worker.start()
            self._workers[worker.pid] = worker

        # Start processing responses
        self._wakeup_task = None
        self._process_responses()

    @syncify
    async def _process_responses(
        self, coro_get: Awaitable[InferenceResponseMessage] = None
    ):
        if coro_get is not None:
            # Process the `.coro_get()` task that was used to get pinged whenever a
            # new message is available.
            try:
                latest_response = await coro_get
                # If the queue gets terminated, detect the "sentinel value" and
                # stop reading
                if latest_response is END_OF_QUEUE:
                    return
            except CancelledError:
                # In the case where the `_wakeup_task` gets canceled (e.g. when
                # closing the worker), the output of the `coro_get` task will be an
                # exception.
                return

            await self._process_response(latest_response)

        while not self._responses.empty():
            response = await self._responses.coro_get()
            await self._process_response(response)

        # Chain next (future) update once we're done processing the queue
        self._wakeup_task = self._responses.coro_get()
        self._wakeup_task.add_done_callback(self._process_responses)

    async def _process_response(self, response: InferenceResponseMessage):
        internal_id = response.id
        # TODO: Raise error if internal id not found
        async_response = self._async_responses[internal_id]

        # TODO: How should inference errors be transmitted back?
        async_response.set_result(response.inference_response)

    async def predict(
        self, model_settings: ModelSettings, inference_request: InferenceRequest
    ) -> InferenceResponse:
        internal_id = generate_uuid()

        model_version = None
        if model_settings.parameters:
            model_version = model_settings.parameters.version

        request_message = InferenceRequestMessage(
            id=internal_id,
            model_name=model_settings.name,
            model_version=model_version,
            inference_request=inference_request,
        )
        await self._requests.coro_put(request_message)

        loop = asyncio.get_running_loop()
        async_response = loop.create_future()
        self._async_responses[internal_id] = async_response

        return await self._wait_response(internal_id)

    async def _wait_response(self, internal_id: str) -> InferenceResponse:
        async_response = self._async_responses[internal_id]

        try:
            inference_response = await async_response
            return inference_response
        finally:
            del self._async_responses[internal_id]

        return await async_response

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

            # TODO: Double check that the model has been loaded in the pool
            # Any reason why not? Should we let the user disable parallel
            # inference per model?
            return await self.predict(model.settings, payload)

        return _inner

    async def load_model(self, model: MLModel) -> MLModel:
        await asyncio.gather(
            *[self._load_model(model, worker) for worker in self._workers.values()]
        )

        # Decorate predict method
        setattr(model, "predict", self.parallel(model.predict))

    async def _load_model(self, model: MLModel, worker: Worker):
        load_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Load, model_settings=model.settings
        )
        await worker.model_updates.coro_put(load_message)
        await worker.model_updates.coro_join()

    async def unload_model(self, model: MLModel) -> MLModel:
        await asyncio.gather(
            *[self._unload_model(model, worker) for worker in self._workers.values()]
        )

    async def _unload_model(self, model: MLModel, worker: Worker):
        unload_message = ModelUpdateMessage(
            update_type=ModelUpdateType.Unload, model_settings=model.settings
        )
        await worker.model_updates.coro_put(unload_message)
        await worker.model_updates.coro_join()

    async def close(self):
        await self._close_workers()
        await self._close_responses()

    async def _close_responses(self):
        await terminate_queue(self._responses)
        if self._wakeup_task is not None:
            # Cancel task awaiting for responses
            await cancel_task(self._wakeup_task)
            self._wakeup_task = None

    async def _close_workers(self):
        # First send N sentinel values (one per worker) to each of the input
        # queues
        await asyncio.gather(
            *[
                asyncio.gather(
                    terminate_queue(worker.model_updates),
                    terminate_queue(self._requests),
                )
                for worker in self._workers.values()
            ]
        )

        # Afterwards, verify that all workers have stopped and remove them from
        # the pool
        for pid, worker in self._workers.items():
            worker.join()

        self._workers.clear()
