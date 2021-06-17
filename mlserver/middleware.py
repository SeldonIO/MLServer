from typing import Callable, List

from .codecs.middleware import codec_middleware
from .settings import ModelSettings
from .types import InferenceRequest

MiddlewareFunc = Callable[[InferenceRequest, ModelSettings], InferenceRequest]
InferenceMiddlewares: List[MiddlewareFunc] = [codec_middleware]


def inference_middlewares(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    for middleware in InferenceMiddlewares:
        request = middleware(request, model_settings)

    return request
