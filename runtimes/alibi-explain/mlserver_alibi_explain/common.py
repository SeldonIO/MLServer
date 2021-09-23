import asyncio
from asyncio import AbstractEventLoop
from enum import Enum

#from mlserver_alibi_explain.explainers.anchor_image import AnchorImageWrapper
#from mlserver import MLModel
from typing import Any, Dict, Optional, Type, Callable, Coroutine, Awaitable

import numpy as np
import requests
from pydantic import BaseSettings

from mlserver.types import ResponseOutput, InferenceResponse, InferenceRequest

_ANCHOR_IMAGE_TAG = 'anchor_image'

ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"


class ExplainerEnum(str, Enum):
    anchor_image = _ANCHOR_IMAGE_TAG


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
        # TODO: proper error handling
        raise ValueError(f"{response_raw.status_code} / {response_raw.reason}")
    return InferenceResponse.parse_raw(response_raw.text)


def execute_async(
        fn: Callable, data: Any, loop: Optional[AbstractEventLoop] = None
) -> Awaitable:
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, fn, data)

# _TAG_TO_IMPL = {
#     _ANCHOR_IMAGE_TAG: type(AnchorImageWrapper)
# }
#
#
# def get_mlmodel_class(tag: ExplainerEnum) -> type(MLModel):
#     return _TAG_TO_IMPL[tag.value]


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    infer_uri: Optional[str]
    init_explainer: bool
    explainer_type: ExplainerEnum
    call_parameters: Optional[dict]
    init_parameters: Optional[dict]