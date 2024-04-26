from functools import wraps
from typing import Awaitable, Callable, Optional, AsyncIterable

from ..errors import MLServerError
from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..utils import get_wrapped_method
from .adaptive import AdaptiveBatcher
from ..logging import logger

_AdaptiveBatchingAttr = "__adaptive_batching__"


class InvalidBatchingMethod(MLServerError):
    def __init__(self, method_name: str, reason: Optional[str] = None):
        msg = f"Method {method_name} can't be used for adaptive batching"
        if reason:
            msg += f": {reason}"

        super().__init__(msg)


def _get_batcher(f: Callable) -> AdaptiveBatcher:
    wrapped_f = get_wrapped_method(f)
    model = _get_model(f)

    if not hasattr(model, _AdaptiveBatchingAttr):
        raise InvalidBatchingMethod(
            wrapped_f.__name__, reason="adaptive batching has not been loaded"
        )

    return getattr(model, _AdaptiveBatchingAttr)


def _get_model(f: Callable) -> MLModel:
    wrapped_f = get_wrapped_method(f)
    if not hasattr(wrapped_f, "__self__"):
        raise InvalidBatchingMethod(wrapped_f.__name__, reason="method is not bound")

    return getattr(wrapped_f, "__self__")


def adaptive_batching(f: Callable[[InferenceRequest], Awaitable[InferenceResponse]]):
    """
    Decorator for the `predict()` method which will ensure it uses the
    underlying adaptive batcher instance.
    """

    @wraps(f)
    async def _inner(payload: InferenceRequest) -> InferenceResponse:
        batcher = _get_batcher(f)
        return await batcher.predict(payload)

    return _inner


def not_implemented_warning(
    f: Callable[[InferenceRequest], AsyncIterable[InferenceResponse]]
):
    """
    Decorator to lets users know that adaptive batching is not enabled on
    method `f`.
    """

    @wraps(f)
    async def _inner(payload: InferenceRequest) -> AsyncIterable[InferenceResponse]:
        model = _get_model(f)
        logger.warning(
            f"Adaptive Batching is enabled for model '{model.name}'"
            " but not supported for inference streaming. "
            "Falling back to non-batched inference streaming."
        )

        yield f(payload)

    return _inner


async def load_batching(model: MLModel) -> MLModel:
    if model.settings.max_batch_size <= 1:
        return model

    if model.settings.max_batch_time <= 0:
        return model

    batcher = AdaptiveBatcher(model)
    setattr(model, _AdaptiveBatchingAttr, batcher)

    # Decorate predict methods
    setattr(model, "predict", adaptive_batching(model.predict))
    setattr(model, "predict_stream", not_implemented_warning(model.predict_stream))
    return model
