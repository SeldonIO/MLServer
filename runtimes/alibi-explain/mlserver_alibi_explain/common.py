import asyncio
import contextvars
import functools
from asyncio import AbstractEventLoop
from enum import Enum
from importlib import import_module
from time import sleep
from typing import Any, Dict, Optional, Type, Callable, Awaitable, Union

import requests
from pydantic import BaseSettings

from mlserver.types import ResponseOutput, InferenceResponse, InferenceRequest

_ANCHOR_IMAGE_TAG = "anchor_image"
_ANCHOR_TEXT_TAG = "anchor_text"
_INTEGRATED_GRADIENTS_TAG = "integrated_gradients"

_TAG_TO_RT_IMPL = {
    _ANCHOR_IMAGE_TAG:
        ("mlserver_alibi_explain.explainers.black_box_runtime.AlibiExplainBlackBoxRuntime",
         "alibi.explainers.AnchorImage"),
    _ANCHOR_TEXT_TAG:
        ("mlserver_alibi_explain.explainers.black_box_runtime.AlibiExplainBlackBoxRuntime",
         "alibi.explainers.AnchorText"),
    _INTEGRATED_GRADIENTS_TAG: (
        "mlserver_alibi_explain.explainers.integrated_gradients.IntegratedGradientsWrapper",
        "alibi.explainers.IntegratedGradients")
}


ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"
EXPLAIN_PARAMETERS_TAG = "explain_parameters"

class ExplainerEnum(str, Enum):
    anchor_image = _ANCHOR_IMAGE_TAG
    anchor_text = _ANCHOR_TEXT_TAG
    integrated_gradients = _INTEGRATED_GRADIENTS_TAG


# TODO: is this inference response?
def create_v2_from_any(data: Any, name: str) -> Dict:
    if isinstance(data, str):
        b = list(bytes(data, "utf-8"))
    else:
        b = list(bytes(repr(data), "utf-8"))
    return {
        "name": name,
        "datatype": "BYTES",
        "data": b,
        "shape": [len(b)],
    }


def convert_from_bytes(output: ResponseOutput, ty: Optional[Type]) -> Any:
    if ty == str:
        return bytearray(output.data).decode("UTF-8")
    else:
        py_str = bytearray(output.data).decode("UTF-8")
        from ast import literal_eval
        return literal_eval(py_str)


def remote_predict(v2_payload: InferenceRequest, predictor_url: str) -> InferenceResponse:
    response_raw = requests.post(predictor_url, json=v2_payload.dict())
    if response_raw.status_code != 200:
        # TODO: add proper error handling
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
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1:])
    return klass
