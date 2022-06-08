from typing import Callable, List

#  from .codecs.middleware import codec_middleware
from .settings import ModelSettings
from .types import InferenceRequest


class InferenceMiddleware:
    """
    Base class to implement middlewares.
    """

    def request_middleware(
        self, request: InferenceRequest, model_settings: ModelSettings
    ) -> InferenceRequest:
        raise NotImplementedError()

    def response_middleware(
        self, response: InferenceResponse, model_settings: ModelSettings
    ) -> InferenceResponse:
        raise NotImplementedError()


class InferenceMiddlewares(InferenceMiddleware):
    """
    Meta-middleware which applies a list of middlewares.
    """

    def __init__(self, inference_middlewares: List[InferenceMiddleware]):
        self._middlewares = inference_middlewares

    def request_middleware(
        self, request: InferenceRequest, model_settings: ModelSettings
    ) -> InferenceRequest:
        for middleware in InferenceMiddlewares:
            request = middleware.request_middleware(request, model_settings)

        return request

    def response_middleware(
        self, response: InferenceResponse, model_settings: ModelSettings
    ) -> InferenceResponse:
        for middleware in InferenceMiddlewares:
            request = middleware.response_middleware(request, model_settings)

        return request
