import asyncio
import os
import json
import contextvars
import functools
from asyncio import AbstractEventLoop
from importlib import import_module
from typing import Optional, Callable, Awaitable, Dict
from distutils.util import strtobool

from pydantic import BaseSettings
from mlserver.errors import MLServerError

from optimum.onnxruntime import (
    ORTModelForCausalLM,
    ORTModelForFeatureExtraction,
    ORTModelForQuestionAnswering,
    ORTModelForSequenceClassification,
    ORTModelForTokenClassification,
)


HUGGINGFACE_TASK_TAG = "task"

ENV_PREFIX_HUGGINGFACE_SETTINGS = "MLSERVER_MODEL_HUGGINGFACE_"
HUGGINGFACE_PARAMETERS_TAG = "huggingface_parameters"
PARAMETERS_ENV_NAME = "PREDICTIVE_UNIT_PARAMETERS"

SUPPORTED_OPTIMIZED_TASKS = {
    "feature-extraction": ORTModelForFeatureExtraction,
    "sentiment-analysis": ORTModelForSequenceClassification,
    "ner": ORTModelForTokenClassification,
    "question-answering": ORTModelForQuestionAnswering,
    "text-generation": ORTModelForCausalLM,
}


class RemoteInferenceError(MLServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(
            f"Remote inference call failed with {code}, {reason}", status_code=code
        )


class InvalidTranformerInitialisation(MLServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(
            f"Remote inference call failed with {code}, {reason}",
            status_code=code,
        )


class HuggingFaceSettings(BaseSettings):
    """
    Parameters that apply only to alibi huggingface models
    """

    class Config:
        env_prefix = ENV_PREFIX_HUGGINGFACE_SETTINGS

    task: str = ""
    pretrained_model: Optional[str] = None
    pretrained_tokenizer: Optional[str] = None
    optimum_model: bool = False


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1 :])
    return klass


def parse_parameters_from_env() -> Dict:
    """
    TODO
    """
    parameters = json.loads(os.environ.get(PARAMETERS_ENV_NAME, "[]"))

    type_dict = {
        "INT": int,
        "FLOAT": float,
        "DOUBLE": float,
        "STRING": str,
        "BOOL": bool,
    }

    parsed_parameters = {}
    for param in parameters:
        name = param.get("name")
        value = param.get("value")
        type_ = param.get("type")
        if type_ == "BOOL":
            parsed_parameters[name] = bool(strtobool(value))
        else:
            try:
                parsed_parameters[name] = type_dict[type_](value)
            except ValueError:
                raise InvalidTranformerInitialisation(
                    "Bad model parameter: "
                    + name
                    + " with value "
                    + value
                    + " can't be parsed as a "
                    + type_,
                    reason="MICROSERVICE_BAD_PARAMETER",
                )
            except KeyError:
                raise InvalidTranformerInitialisation(
                    "Bad model parameter type: "
                    + type_
                    + " valid are INT, FLOAT, DOUBLE, STRING, BOOL",
                    reason="MICROSERVICE_BAD_PARAMETER",
                )
    return parsed_parameters
