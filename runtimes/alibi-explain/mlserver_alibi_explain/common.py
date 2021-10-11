import asyncio
import contextvars
import functools
from asyncio import AbstractEventLoop
from enum import Enum
from importlib import import_module
from typing import Any, Optional, Type, Callable, Awaitable, Union

import requests
from pydantic import BaseSettings

from mlserver.types import ResponseOutput, InferenceResponse, InferenceRequest

EXPLAINER_TYPE_TAG = "explainer_type"

_MAX_RETRY_ATTEMPT = 3

_ANCHOR_IMAGE_TAG = "anchor_image"
_ANCHOR_TEXT_TAG = "anchor_text"
_INTEGRATED_GRADIENTS_TAG = "integrated_gradients"

_TAG_TO_RT_IMPL = {
    _ANCHOR_IMAGE_TAG: (
        "mlserver_alibi_explain.explainers.black_box_runtime.AlibiExplainBlackBoxRuntime",
        "alibi.explainers.AnchorImage",
    ),
    _ANCHOR_TEXT_TAG: (
        "mlserver_alibi_explain.explainers.black_box_runtime.AlibiExplainBlackBoxRuntime",
        "alibi.explainers.AnchorText",
    ),
    _INTEGRATED_GRADIENTS_TAG: (
        "mlserver_alibi_explain.explainers.integrated_gradients.IntegratedGradientsWrapper",
        "alibi.explainers.IntegratedGradients",
    ),
}


ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"
EXPLAIN_PARAMETERS_TAG = "explain_parameters"


class ExplainerEnum(str, Enum):
    anchor_image = _ANCHOR_IMAGE_TAG
    anchor_text = _ANCHOR_TEXT_TAG
    integrated_gradients = _INTEGRATED_GRADIENTS_TAG


def convert_from_bytes(output: ResponseOutput, ty: Optional[Type]) -> Any:
    """
    This utility function decodes the response from bytes string to python object dict.
    It is related to decoding StringCodec
    TODO: add this utility in the codec.
    """
    if ty == str:
        return bytearray(output.data).decode("UTF-8")
    else:
        py_str = bytearray(output.data).decode("UTF-8")
        from ast import literal_eval

        return literal_eval(py_str)


# TODO: add retry
def remote_predict(
    v2_payload: InferenceRequest, predictor_url: str
) -> InferenceResponse:
    response_raw = requests.post(predictor_url, json=v2_payload.dict())
    if response_raw.status_code != 200:
        raise ValueError(f"{response_raw.status_code} / {response_raw.reason}")
    return InferenceResponse.parse_raw(response_raw.text)


# TODO: this is very similar to `asyncio.to_thread` (python 3.9+), so lets use it at some point.
def execute_async(
    loop: Optional[AbstractEventLoop], fn: Callable, *args, **kwargs
) -> Awaitable:
    if loop is None:
        loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, fn, *args, **kwargs)
    return loop.run_in_executor(None, func_call)


def get_mlmodel_class_as_str(tag: Union[ExplainerEnum, str]) -> str:
    if isinstance(tag, ExplainerEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag][0]


def get_alibi_class_as_str(tag: Union[ExplainerEnum, str]) -> str:
    if isinstance(tag, ExplainerEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag][1]


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    infer_uri: Optional[str]
    explainer_type: str
    init_parameters: Optional[dict]


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1 :])
    return klass
