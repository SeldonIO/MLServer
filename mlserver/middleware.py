from .settings import ModelSettings
from .types import InferenceRequest, InferenceResponse


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

    def __init__(self, *inference_middlewares):
        self._middlewares = inference_middlewares

    def request_middleware(
        self, request: InferenceRequest, model_settings: ModelSettings
    ) -> InferenceRequest:
        processed_request = request
        for middleware in self._middlewares:
            processed_request = middleware.request_middleware(
                processed_request, model_settings
            )

        return processed_request

    def response_middleware(
        self, response: InferenceResponse, model_settings: ModelSettings
    ) -> InferenceResponse:
        processed_response = response
        for middleware in self._middlewares:
            processed_response = middleware.response_middleware(
                processed_response, model_settings
            )

        return processed_response
