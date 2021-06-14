from typing import Callable, List

from .codecs.middleware import decode_request_inputs
from .settings import ModelSettings
from .types import InferenceRequest

MiddlewareFunc = Callable[[InferenceRequest, ModelSettings], InferenceRequest]
InferenceMiddlewares: List[MiddlewareFunc] = [decode_request_inputs]


def inference_middlewares(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    for middleware in InferenceMiddlewares:
        request = middleware(request, model_settings)

    return request
