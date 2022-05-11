import asyncio

from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue
from functools import wraps
from typing import Any, Dict, Coroutine, Callable

from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings, ModelSettings
from ..utils import get_wrapped_method, generate_uuid
from ..errors import InferenceError

from .errors import InvalidParallelMethod
from .worker import Worker
from .utils import END_OF_QUEUE, terminate_queue, cancel_task, configure_inference_pool
from .messages import (
    InferenceRequestMessage,
    InferenceResponseMessage,
    ModelUpdateMessage,
    ModelUpdateType,
)
from .logging import logger


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

        self._workers = {}
        self._settings = settings
        self._requests: Queue[InferenceRequestMessage] = Queue()
        self._responses: Queue[InferenceResponseMessage] = Queue()
        self._async_responses: Dict[str, Future[InferenceResponse]] = {}
        self._executor = ThreadPoolExecutor()
        for idx in range(self._settings.parallel_workers):
            # TODO: Set callback to restart worker if it goes down (would
            # `worker.join` help with that?)
            worker = Worker(self._requests, self._responses)
            worker.start()
            self._workers[worker.pid] = worker

        # Start processing responses
        self._start_processing_responses()

    def _start_processing_responses(self):
        self._active = True
        self._process_responses_task = asyncio.create_task(self._process_responses())
        self._process_responses_task.add_done_callback(self._process_responses_cb)

    def _process_responses_cb(self, process_responses):
        try:
            process_responses.result()
        except asyncio.CancelledError:
            # NOTE: The response loop was cancelled from the outside, so don't
            # restart
            return
        except Exception:
            logger.exception("Response processing loop crashed. Restarting the loop...")
            # If process loop crashed, restart it
            self._start_processing_responses()

    async def _process_responses(self):
        logger.debug("Starting response processing loop...")
        loop = asyncio.get_event_loop()
        while self._active:
            response = await loop.run_in_executor(self._executor, self._responses.get)

            # If the queue gets terminated, detect the "sentinel value" and
            # stop reading
            if response is END_OF_QUEUE:
                return

            await self._process_response(response)

    async def _process_response(self, response: InferenceResponseMessage):
        internal_id = response.id

        async_response = self._async_responses[internal_id]

        if response.inference_response:
            async_response.set_result(response.inference_response)
        elif response.exception:
            async_response.set_exception(response.exception)
        else:
            exc = InferenceError("Inference returned no value")
            async_response.set_exception(exc)

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
        self._requests.put(request_message)

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
        # NOTE: This is a remnant from the previous architecture for parallel
        # workers, where each worker had its own pool.
        # For backwards compatibility, we will respect when a model disables
        # parallel inference.
        if not model.settings.parallel_workers:
            return False

        if not self._settings.parallel_workers:
            return False

        return True

    async def close(self):
        await self._close_workers()
        await self._close_responses()

    async def _close_responses(self):
        await terminate_queue(self._responses)
        await cancel_task(self._process_responses_task)
        self._responses.close()
        self._requests.close()
        self._executor.shutdown()

    async def _close_workers(self):
        # First close down model updates loop
        for pid, worker in self._workers.items():
            await worker.stop()
            worker.join()

        self._workers.clear()
