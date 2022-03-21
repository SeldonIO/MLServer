from typing import Any, Coroutine, Callable, Optional
from aioprocessing import AioQueue, AioJoinableQueue

from ..types import InferenceRequest, InferenceResponse
from ..settings import Settings, ModelSettings
from ..utils import get_wrapped_method

from .worker import Worker

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
        for idx in range(parallel_workers):
            # TODO: Set callback to restart worker if it goes down (would
            # `worker.join` help with that?)
            model_updates = AioJoinableQueue()
            worker = Worker(self._requests, self._responses, model_updates)
            worker.start()
            self._workers[worker.pid] = worker

    def predict(
        self, model_settings: ModelSettings, payload: InferenceRequest
    ) -> InferenceResponse:
        pass

    async def parallel(self, f: PredictMethod):
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
