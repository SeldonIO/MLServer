from typing import Callable, List, Any
from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

#  from .codecs.middleware import codec_middleware
from .settings import ModelSettings
from .types import InferenceRequest
from .cloudevents import cloudevents_middleware

MiddlewareFunc = Callable[[InferenceRequest, ModelSettings], InferenceRequest]
#  InferenceMiddlewares: List[MiddlewareFunc] = [codec_middleware]
# NOTE: Remove codecs temporarily from middleware to reduce serialisation
# overhead when sending payload to inference workers.
InferenceMiddlewares: List[MiddlewareFunc] = []


def inference_middlewares(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    for middleware in InferenceMiddlewares:
        request = middleware(request, model_settings)

    return request


FastAPIMiddlewareFunc = Callable[[Request, Any], None]
FastAPIMiddlewares: List[FastAPIMiddlewareFunc] = [cloudevents_middleware]


def add_fastapi_middleware(app: FastAPI):
    """
    Inference middlewares get called as part of DataPlane.infer
    as opposed to as a FastAPI middleware given that the expected
    parameters are the post-processed ones as InferenceResponse /
    InferenceResponse as opposed to raw requests
    """
    for middleware in FastAPIMiddlewares:
        app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)
