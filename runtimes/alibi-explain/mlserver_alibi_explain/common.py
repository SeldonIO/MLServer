import re
from importlib import import_module
from typing import Any, Optional, Type, Union, List

import numpy as np
import requests
from pydantic import BaseSettings

from mlserver.codecs import StringCodec, NumpyCodec
from mlserver.types import (
    ResponseOutput,
    InferenceResponse,
    InferenceRequest,
    Parameters,
    MetadataModelResponse,
    RequestOutput,
)
from mlserver.utils import generate_uuid

from mlserver_alibi_explain.errors import RemoteInferenceError, InvalidExplanationShape

_DEFAULT_INPUT_NAME = "predict"

EXPLAINER_TYPE_TAG = "explainer_type"

ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"
EXPLAIN_PARAMETERS_TAG = "explain_parameters"
SELDON_SKIP_LOGGING_HEADER = "Seldon-Skip-Logging"


#  TODO: add this utility in the codec.
def convert_from_bytes(output: ResponseOutput, ty: Optional[Type] = None) -> Any:
    """
    This utility function decodes the response from bytes string to python object dict.
    It is related to decoding StringCodec
    """
    if output.shape not in ([1], [1, 1]):
        raise InvalidExplanationShape(output.shape)

    if ty == str:
        return bytearray(output.data[0]).decode("UTF-8")
    else:
        py_str = bytearray(output.data[0]).decode("UTF-8")

        from ast import literal_eval

        return literal_eval(py_str)


# TODO: add retry and better exceptions handling
def remote_predict(
    v2_payload: InferenceRequest, predictor_url: str, ssl_verify_path: str
) -> InferenceResponse:
    verify: Union[str, bool] = True
    if ssl_verify_path != "":
        verify = ssl_verify_path
    response_raw = requests.post(
        predictor_url,
        json=v2_payload.dict(),
        headers={SELDON_SKIP_LOGGING_HEADER: "true"},
        verify=verify,
    )
    if response_raw.status_code != 200:
        raise RemoteInferenceError(response_raw.status_code, response_raw.reason)
    return InferenceResponse.parse_raw(response_raw.text)


def remote_metadata(url: str, ssl_verify_path: str) -> MetadataModelResponse:
    """Get metadata from v2 endpoint"""
    verify: Union[str, bool] = True
    if ssl_verify_path != "":
        verify = ssl_verify_path
    response_raw = requests.get(url, verify=verify)
    if response_raw.status_code != 200:
        raise RemoteInferenceError(response_raw.status_code, response_raw.reason)
    return MetadataModelResponse.parse_raw(response_raw.text)


def construct_metadata_url(infer_url: str) -> str:
    """Construct v2 metadata endpoint from v2 infer endpoint"""
    return re.sub(r"/infer$", "", infer_url)


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    infer_uri: str
    explainer_type: str
    explainer_batch: Optional[bool] = False
    # In cases where the inference model can output multiple fields and
    # we are interested in a specific field for explanation
    infer_output: Optional[str]
    init_parameters: Optional[dict]
    ssl_verify_path: Optional[str]


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1 :])
    return klass


def to_v2_inference_request(
    input_data: Union[np.ndarray, List[str]],
    metadata: Optional[MetadataModelResponse],
    output: Optional[str],
) -> InferenceRequest:
    """
    Encode numpy payload to v2 protocol.

    If `output` is set, it takes precedence over any outputs that are set in the
    `metadata` given that the user then is explicitly defining an output.

    Note: We only fetch the first-input name and the list of outputs from the metadata
    endpoint currently. We should consider wider reconciliation with data types etc.

    Parameters
    ----------
    input_data
       Numpy ndarray to encode
    metadata
       Extra metadata that can help encode the payload.
    output
       The output we care about to explain from the inference model.
    """

    # MLServer does not really care about a correct input name!
    input_name = _DEFAULT_INPUT_NAME
    id_name = generate_uuid()
    default_outputs = []
    outputs = []

    if output:
        outputs = [RequestOutput(name=output)]

    if metadata is not None:
        if metadata.inputs:
            # we only support a big single input numpy
            input_name = metadata.inputs[0].name
        if metadata.outputs:
            if not output:
                default_outputs = [metadata.outputs[0]]

    # For List[str] (e.g. AnchorText), we use StringCodec for input
    input_payload_codec = StringCodec if type(input_data) == list else NumpyCodec
    v2_request = InferenceRequest(
        id=id_name,
        parameters=Parameters(content_type=input_payload_codec.ContentType),
        # TODO: we probably need to tell alibi about the expected types to use
        # or even whether it is a probability of classes or targets etc
        inputs=[
            input_payload_codec.encode_input(  # type: ignore
                name=input_name,
                payload=input_data,
                use_bytes=False,
            )
        ],
        outputs=outputs if outputs else default_outputs,
    )
    return v2_request
