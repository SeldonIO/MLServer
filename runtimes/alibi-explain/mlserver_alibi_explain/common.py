import asyncio
from asyncio import AbstractEventLoop
from enum import Enum
from typing import Any, Dict, Optional, Type, Callable, Awaitable

import requests
from pydantic import BaseSettings

from mlserver.types import ResponseOutput, InferenceResponse, InferenceRequest

_ANCHOR_IMAGE_TAG = 'anchor_image'

_TAG_TO_RT_IMPL = {
    # TODO: add a test to make sure these represent real classes
    _ANCHOR_IMAGE_TAG:
        ("mlserver_alibi_explain.explainers.black_box_runtime.AlibiExplainBlackBoxRuntime",
         "alibi.explainers.AnchorImage"),
}


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
        # TODO: add proper error handling
        raise ValueError(f"{response_raw.status_code} / {response_raw.reason}")
    return InferenceResponse.parse_raw(response_raw.text)


def execute_async(
        loop: Optional[AbstractEventLoop], fn: Callable, input_data: Any, settings: BaseSettings
) -> Awaitable:
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, fn, input_data, settings)


def get_mlmodel_class_as_str(tag: ExplainerEnum) -> str:
    return _TAG_TO_RT_IMPL[tag.value][0]


def get_alibi_class_as_str(tag: ExplainerEnum) -> str:
    return _TAG_TO_RT_IMPL[tag.value][1]


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    # TODO add black box settings?
    infer_uri: Optional[str]
    init_explainer: bool
    explainer_type: ExplainerEnum
    init_parameters: Optional[dict]
