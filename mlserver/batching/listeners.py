from functools import wraps
from typing import Any, Callable, Coroutine, Optional

from ..errors import MLServerError
from ..model import MLModel
from ..types import InferenceRequest, InferenceResponse
from .adaptive import AdaptiveBatcher

_AdaptiveBatchingAttr = "__adaptive_batching__"


class InvalidBatchingMethod(MLServerError):
    def __init__(self, method_name: str, reason: Optional[str] = None):
        msg = f"Method {method_name} can't be used for adaptive batching"
        if reason:
            msg += f": {reason}"

        super().__init__(msg)


def adaptive_batching(
    f: Callable[[InferenceRequest], Coroutine[Any, Any, InferenceResponse]]
):
    """
    Decorator to attach to model's methods so that they run in parallel.
    By default, this will get attached to every model's "inference" method.

    NOTE: At the moment, this method only works with `predict()`.
    """
    # TODO: Extend to multiple methods
    @wraps(f)
    async def _inner(payload: InferenceRequest) -> InferenceResponse:
        if not hasattr(f, "__self__"):
            raise InvalidBatchingMethod(f.__name__, reason="method is not bound")

        model = getattr(f, "__self__")
        if not hasattr(model, _AdaptiveBatchingAttr):
            raise InvalidBatchingMethod(
                f.__name__, reason="adaptive batching has not been loaded"
            )

        pool = getattr(model, _AdaptiveBatchingAttr)
        return await pool.predict(payload)

    return _inner


def load_batching(model: MLModel) -> MLModel:
    # TODO: Check whether adaptive batching is disabled
    batcher = AdaptiveBatcher(model)
    setattr(model, _AdaptiveBatchingAttr, batcher)

    # Decorate predict method
    setattr(model, "predict", adaptive_batching(model.predict))

    return model
