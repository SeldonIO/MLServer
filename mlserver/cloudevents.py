from enum import Enum
from typing import Dict, Optional, Union

from .settings import Settings, ModelSettings
from .types import InferenceRequest, InferenceResponse, Parameters
from .middleware import InferenceMiddleware

CLOUDEVENTS_HEADER_ID = "Ce-Id"
CLOUDEVENTS_HEADER_SPECVERSION = "Ce-Specversion"
CLOUDEVENTS_HEADER_SOURCE = "Ce-Source"
CLOUDEVENTS_HEADER_TYPE = "Ce-Type"
CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT = "0.3"

CLOUDEVENTS_HEADER_REQUEST_ID = "Ce-Requestid"
CLOUDEVENTS_HEADER_MODEL_ID = "Ce-Modelid"
CLOUDEVENTS_HEADER_INFERENCE_SERVICE = "Ce-Inferenceservicename"
CLOUDEVENTS_HEADER_NAMESPACE = "Ce-Namespace"
CLOUDEVENTS_HEADER_ENDPOINT = "Ce-Endpoint"


class CloudEventsTypes(Enum):
    Request = "io.seldon.serving.inference.request"
    Response = "io.seldon.serving.inference.response"


def get_namespace() -> Optional[str]:
    try:
        # Namespace can be fetched from loaded file vars from k8s 1.15.3+
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

    return None


def _update_headers(
    payload: Union[InferenceRequest, InferenceResponse], headers: Dict[str, str]
):
    if payload.parameters is None:
        payload.parameters = Parameters(headers=headers)
        return

    if payload.parameters.headers is None:
        payload.parameters.headers = headers
        return

    payload.parameters.headers.update(headers)


class CloudEventsMiddleware(InferenceMiddleware):
    def __init__(self, settings: Settings):
        self._settings = settings
        self._namespace = get_namespace()

    def _get_headers(
        self,
        ce_type: CloudEventsTypes,
        model_settings: ModelSettings,
        ce_id: Optional[str],
    ) -> Dict[str, str]:
        source = f"io.seldon.serving.deployment.{self._settings.server_name}"
        if self._namespace:
            source = f"{source}.{self._namespace}"

        ce_headers = {
            CLOUDEVENTS_HEADER_SPECVERSION: CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT,
            CLOUDEVENTS_HEADER_SOURCE: source,
            CLOUDEVENTS_HEADER_TYPE: ce_type.value,
            CLOUDEVENTS_HEADER_MODEL_ID: model_settings.name,
            CLOUDEVENTS_HEADER_INFERENCE_SERVICE: self._settings.server_name,
            CLOUDEVENTS_HEADER_ENDPOINT: model_settings.name,
        }

        if ce_id:
            ce_headers[CLOUDEVENTS_HEADER_ID] = ce_id
            ce_headers[CLOUDEVENTS_HEADER_REQUEST_ID] = ce_id

        if self._namespace:
            ce_headers[CLOUDEVENTS_HEADER_NAMESPACE] = self._namespace

        return ce_headers

    def request_middleware(
        self,
        request: InferenceRequest,
        model_settings: ModelSettings,
    ) -> InferenceRequest:
        ce_headers = self._get_headers(
            CloudEventsTypes.Request, model_settings, request.id
        )

        _update_headers(request, ce_headers)
        return request

    def response_middleware(
        self,
        response: InferenceResponse,
        model_settings: ModelSettings,
    ) -> InferenceResponse:
        ce_headers = self._get_headers(
            CloudEventsTypes.Response, model_settings, response.id
        )

        _update_headers(response, ce_headers)
        return response
