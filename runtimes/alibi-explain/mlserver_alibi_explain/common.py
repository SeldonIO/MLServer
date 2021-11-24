import asyncio
import contextvars
import functools
import re
from asyncio import AbstractEventLoop
from importlib import import_module
from typing import Any, Optional, Type, Callable, Awaitable, Union, List

import numpy as np
import requests
from pydantic import BaseSettings

from mlserver.codecs import StringCodec, NumpyCodec
from mlserver.errors import RemoteInferenceError
from mlserver.types import (
    ResponseOutput,
    InferenceResponse,
    InferenceRequest,
    Parameters,
    MetadataModelResponse,
)

_DEFAULT_ID_NAME = "explain_inference"

_DEFAULT_INPUT_NAME = "predict"

EXPLAINER_TYPE_TAG = "explainer_type"

_MAX_RETRY_ATTEMPT = 3

ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"
EXPLAIN_PARAMETERS_TAG = "explain_parameters"


#  TODO: add this utility in the codec.
def convert_from_bytes(output: ResponseOutput, ty: Optional[Type]) -> Any:
    """
    This utility function decodes the response from bytes string to python object dict.
    It is related to decoding StringCodec
    """
    if ty == str:
        return bytearray(output.data).decode("UTF-8")
    else:
        py_str = bytearray(output.data).decode("UTF-8")
        from ast import literal_eval

        return literal_eval(py_str)


# TODO: add retry and better exceptions handling
def remote_predict(
    v2_payload: InferenceRequest, predictor_url: str
) -> InferenceResponse:
    response_raw = requests.post(predictor_url, json=v2_payload.dict())
    if response_raw.status_code != 200:
        raise RemoteInferenceError(response_raw.status_code, response_raw.reason)
    return InferenceResponse.parse_raw(response_raw.text)


def remote_metadata(url: str) -> MetadataModelResponse:
    """Get metadata from v2 endpoint"""
    response_raw = requests.get(url)
    if response_raw.status_code != 200:
        raise RemoteInferenceError(response_raw.status_code, response_raw.reason)
    return MetadataModelResponse.parse_raw(response_raw.text)


def construct_metadata_url(infer_url: str) -> str:
    """Construct v2 metadata endpoint from v2 infer endpoint"""
    return re.sub(r"/infer$", "", infer_url)


# TODO: this is very similar to `asyncio.to_thread` (python 3.9+),
# so lets use it at some point.
def execute_async(
    loop: Optional[AbstractEventLoop], fn: Callable, *args, **kwargs
) -> Awaitable:
    if loop is None:
        loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, fn, *args, **kwargs)
    return loop.run_in_executor(None, func_call)


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    infer_uri: str
    explainer_type: str
    init_parameters: Optional[dict]


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1 :])
    return klass


def to_v2_inference_request(
    input_data: Union[np.ndarray, List[str]],
    metadata: Optional[MetadataModelResponse],
) -> InferenceRequest:
    """
    Encode numpy payload to v2 protocol.

    Note: We only fetch the first-input name and the list of outputs from the metadata
    endpoint currently. We should consider wider reconciliation with data types etc.

    Parameters
    ----------
    input_data
       Numpy ndarray to encode
    metadata
       Extra metadata that can help encode the payload.
    """

    # MLServer does not really care about a correct input name!
    input_name = _DEFAULT_INPUT_NAME
    id_name = _DEFAULT_ID_NAME
    outputs = []

    if metadata is not None:
        if metadata.inputs:
            # we only support a big single input numpy
            input_name = metadata.inputs[0].name
        if metadata.outputs:
            outputs = metadata.outputs

    # For List[str] (e.g. AnchorText), we use StringCodec for input
    input_payload_codec = StringCodec if type(input_data) == list else NumpyCodec
    v2_request = InferenceRequest(
        id=id_name,
        parameters=Parameters(content_type=input_payload_codec.ContentType),
        # TODO: we probably need to tell alibi about the expected types to use
        # or even whether it is a probability of classes or targets etc
        inputs=[
            input_payload_codec.encode_request_input(  # type: ignore
                name=input_name, payload=input_data
            )
        ],
        # set outputs as empty list, this will return everything?
        outputs=outputs,
    )
    return v2_request
