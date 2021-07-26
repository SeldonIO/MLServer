import asyncio

from functools import wraps
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Coroutine, Callable

from .settings import ModelSettings
from .model import MLModel
from .types import InferenceRequest, InferenceResponse

_InferencePoolAttr = "__inference_pool__"


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


class InferencePool:
    """
    The InferencePool class represents a pool of workers where we can run
    inference on.

    Under the hood, it's responsible for managing a pool of multiprocessing
    workers, where the model is loaded.
    This approach lets MLServer work around the GIL to make sure that inference
    can occur in parallel across multiple models or instances of a model.
    """

    def __init__(self, model: MLModel):
        # TODO: Read the number of workers from the model settings
        self._executor = ProcessPoolExecutor(
            initializer=_mp_load, initargs=(model._settings,)
        )

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # What if we serialise payload?
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, _mp_predict, payload)

    def __del__(self):
        self._executor.shutdown(wait=True)


def parallel(f: Callable[[InferenceRequest], Coroutine[Any, Any, InferenceResponse]]):
    """
    Decorator to attach to model's methods so that they run in parallel.
    By default, this will get attached to every model's "inference" method.

    NOTE: At the moment, this method only works with `predict()`.
    """
    # TODO: Extend to multiple methods
    @wraps(f)
    async def _inner(payload: InferenceRequest) -> InferenceResponse:
        # Method should be bound
        # TODO: Raise if method not bound or if pool is missing
        self = f.__self__
        pool = getattr(self, _InferencePoolAttr)

        if pool is None:
            # TODO: Raise error
            return await f(payload)

        return await pool.predict(payload)

    return _inner


async def load_inference_pool(model: MLModel):
    pool = InferencePool(model)
    setattr(model, _InferencePoolAttr, pool)

    # Override predict pool
    model.predict = parallel(model.predict)

    return model


async def unload_inference_pool(model: MLModel):
    pool = getattr(model, _InferencePoolAttr)
    if not pool:
        return

    pool.__del__()
    delattr(model, _InferencePoolAttr)
