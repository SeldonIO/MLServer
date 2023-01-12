import os
import json
from typing import Optional, Dict
from distutils.util import strtobool

import numpy as np
from pydantic import BaseSettings
from mlserver.errors import MLServerError

from transformers.pipelines import pipeline
from transformers.pipelines.base import Pipeline
from transformers.models.auto.tokenization_auto import AutoTokenizer

from optimum.pipelines import SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS


HUGGINGFACE_TASK_TAG = "task"

ENV_PREFIX_HUGGINGFACE_SETTINGS = "MLSERVER_MODEL_HUGGINGFACE_"
HUGGINGFACE_PARAMETERS_TAG = "huggingface_parameters"
PARAMETERS_ENV_NAME = "PREDICTIVE_UNIT_PARAMETERS"


class InvalidTranformerInitialisation(MLServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(
            f"Huggingface server failed with {code}, {reason}",
            status_code=code,
        )


class HuggingFaceSettings(BaseSettings):
    """
    Parameters that apply only to alibi huggingface models
    """

    class Config:
        env_prefix = ENV_PREFIX_HUGGINGFACE_SETTINGS

    task: str = ""
    # Why need this filed?
    # for translation task, required a suffix to specify source and target
    # related issue: https://github.com/SeldonIO/MLServer/issues/947
    task_suffix: str = ""
    pretrained_model: Optional[str] = None
    pretrained_tokenizer: Optional[str] = None
    optimum_model: bool = False
    device: int = -1
    batch_size: Optional[int] = None

    @property
    def task_name(self):
        if self.task == "translation":
            return f"{self.task}{self.task_suffix}"
        return self.task


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


def load_pipeline_from_settings(hf_settings: HuggingFaceSettings) -> Pipeline:
    """
    TODO
    """
    # TODO: Support URI for locally downloaded artifacts
    # uri = model_parameters.uri
    model = hf_settings.pretrained_model
    tokenizer = hf_settings.pretrained_tokenizer
    device = hf_settings.device

    if model and not tokenizer:
        tokenizer = model

    if hf_settings.optimum_model:
        optimum_class = SUPPORTED_OPTIMUM_TASKS[hf_settings.task]["class"][0]
        model = optimum_class.from_pretrained(
            hf_settings.pretrained_model,
            from_transformers=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        # Device needs to be set to -1 due to known issue
        # https://github.com/huggingface/optimum/issues/191
        device = -1

    pp = pipeline(
        hf_settings.task_name,
        model=model,
        tokenizer=tokenizer,
        device=device,
        batch_size=hf_settings.batch_size,
    )

    # If batch_size > 0 we need to ensure tokens are padded
    if hf_settings.batch_size:
        pp.tokenizer.pad_token_id = [str(pp.model.config.eos_token_id)]  # type: ignore

    return pp


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
