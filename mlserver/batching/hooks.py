from functools import wraps
from typing import Awaitable, Callable, Optional

from ..errors import MLServerError
from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from ..utils import get_wrapped_method
from .adaptive import AdaptiveBatcher

_AdaptiveBatchingAttr = "__adaptive_batching__"


class InvalidBatchingMethod(MLServerError):
    def __init__(self, method_name: str, reason: Optional[str] = None):
        msg = f"Method {method_name} can't be used for adaptive batching"
        if reason:
            msg += f": {reason}"

        super().__init__(msg)


def adaptive_batching(f: Callable[[InferenceRequest], Awaitable[InferenceResponse]]):
    """
    Decorator for the `predict()` method which will ensure it uses the
    underlying adaptive batcher instance.
    """

    @wraps(f)
    async def _inner(payload: InferenceRequest) -> InferenceResponse:
        wrapped_f = get_wrapped_method(f)
        if not hasattr(wrapped_f, "__self__"):
            raise InvalidBatchingMethod(
                wrapped_f.__name__, reason="method is not bound"
            )

        model = getattr(wrapped_f, "__self__")
        if not hasattr(model, _AdaptiveBatchingAttr):
            raise InvalidBatchingMethod(
                wrapped_f.__name__, reason="adaptive batching has not been loaded"
            )

        batcher = getattr(model, _AdaptiveBatchingAttr)
        return await batcher.predict(payload)

    return _inner


async def load_batching(model: MLModel):
    if model.settings.max_batch_size <= 1:
        return None

    if model.settings.max_batch_time <= 0:
        return None

    batcher = AdaptiveBatcher(model)
    setattr(model, _AdaptiveBatchingAttr, batcher)

    # Decorate predict method
    setattr(model, "predict", adaptive_batching(model.predict))
