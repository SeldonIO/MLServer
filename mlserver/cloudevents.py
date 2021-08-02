import os
from typing import Dict

from .types import InferenceResponse
from .settings import ModelSettings

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

ENV_SDEP_NAME = "SELDON_DEPLOYMENT_ID"
ENV_PREDICTOR_NAME = "PREDICTOR_ID"
ENV_MODEL_NAME = "PREDICTIVE_UNIT_ID"

NOT_IMPLEMENTED_STR = "NOTIMPLEMENTED"

env_sdep_name = os.getenv(ENV_SDEP_NAME, NOT_IMPLEMENTED_STR)
env_predictor_name = os.getenv(ENV_PREDICTOR_NAME, NOT_IMPLEMENTED_STR)
env_model_name = os.getenv(ENV_MODEL_NAME, NOT_IMPLEMENTED_STR)

# Namespace can be fetched from loaded file vars from k8s 1.15.3+
try:
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
        env_namespace = f.read()
except Exception:
    env_namespace = "NOTIMPLEMENTED"


# TODO: Add types
def get_cloudevent_headers(request_id: str, ce_type: str) -> Dict:
    """Retrieve the cloud events as dictionary

    Parameters
    ----------
    request_id
     String containing the ID of the request to send as part of the header.
    ce_type
     String containing the value from the InsightsTypes class value.

    Returns
    -------
    Dictionary containing the headers names as keys and respective values accordingly
    """

    ce = {
        CLOUDEVENTS_HEADER_ID: request_id,
        CLOUDEVENTS_HEADER_SPECVERSION: CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT,
        # TODO: Confirm whether we want URL or source - Currently don't have access to URL
        CLOUDEVENTS_HEADER_SOURCE: f"io.seldon.serving.deployment.{env_sdep_name}.{env_namespace}",
        CLOUDEVENTS_HEADER_TYPE: ce_type,
        CLOUDEVENTS_HEADER_REQUEST_ID: request_id,
        CLOUDEVENTS_HEADER_MODEL_ID: env_model_name,
        CLOUDEVENTS_HEADER_INFERENCE_SERVICE: env_sdep_name,
        CLOUDEVENTS_HEADER_NAMESPACE: env_namespace,
        CLOUDEVENTS_HEADER_ENDPOINT: env_predictor_name,
    }
    return ce


def cloudevents_middleware(
    response: InferenceResponse, model_settings: ModelSettings
) -> InferenceResponse:

    return response

