from typing import Callable, List

#  from .codecs.middleware import codec_middleware
from .settings import ModelSettings
from .types import InferenceRequest, InferenceResponse
from .cloudevents import cloudevents_middleware

MiddlewareRequestFunc = Callable[[InferenceRequest, ModelSettings], InferenceRequest]
#  InferenceRequestMiddlewares: List[MiddlewareRequestFunc] = [codec_middleware]
# NOTE: Remove codecs temporarily from middleware to reduce serialisation
# overhead when sending payload to inference workers.
InferenceRequestMiddlewares: List[MiddlewareRequestFunc] = []


def inference_request_middlewares(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    """
    Inference middlewares get called as part of DataPlane.infer
    as opposed to as a FastAPI middleware given that the expected
    parameters are the post-processed ones as InferenceRequest /
    InferenceResponse as opposed to raw requests
    """
    for middleware in InferenceRequestMiddlewares:
        request = middleware(request, model_settings)

    return request


MiddlewareResponseFunc = Callable[[InferenceResponse, ModelSettings], InferenceResponse]
InferenceResponseMiddlewares: List[MiddlewareResponseFunc] = [cloudevents_middleware]


def inference_response_middlewares(
    response: InferenceResponse, model_settings: ModelSettings
) -> InferenceResponse:
    """
    Inference middlewares get called as part of DataPlane.infer
    as opposed to as a FastAPI middleware given that the expected
    parameters are the post-processed ones as InferenceResponse /
    InferenceResponse as opposed to raw requests
    """
    for middleware in InferenceResponseMiddlewares:
        response = middleware(response, model_settings)

    return response


