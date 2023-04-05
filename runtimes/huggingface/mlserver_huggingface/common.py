import os
import json
from typing import Callable, Optional, Dict
from distutils.util import strtobool

import numpy as np
from pydantic import BaseSettings
from functools import partial
from mlserver.errors import MLServerError
from mlserver.settings import ModelSettings

from optimum.pipelines import pipeline as opt_pipeline
from transformers.pipelines import pipeline as trf_pipeline
from transformers.pipelines.base import Pipeline

try:
    # Optimum 1.7 changed the import name from `SUPPORTED_TASKS` to
    # `ORT_SUPPORTED_TASKS`.
    # We'll try to import the more recent one, falling back to the previous
    # import name if not present.
    # https://github.com/huggingface/optimum/blob/987b02e4f6e2a1c9325b364ff764da2e57e89902/optimum/pipelines/__init__.py#L18
    from optimum.pipelines import ORT_SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS
except ImportError:
    from optimum.pipelines import SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS


OPTIMUM_ACCELERATOR = "ort"
ENV_PREFIX_HUGGINGFACE_SETTINGS = "MLSERVER_MODEL_HUGGINGFACE_"
PARAMETERS_ENV_NAME = "PREDICTIVE_UNIT_PARAMETERS"

_PipelineConstructor = Callable[..., Pipeline]


class InvalidTranformerInitialisation(MLServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(
            f"Huggingface server failed with {code}, {reason}",
            status_code=code,
        )


class HuggingFaceSettings(BaseSettings):
    """
    Parameters that apply only to HuggingFace models
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
    framework: Optional[str] = None
    optimum_model: bool = False
    device: int = -1

    @property
    def task_name(self):
        if self.task == "translation":
            return f"{self.task}{self.task_suffix}"
        return self.task


def parse_parameters_from_env() -> Dict:
    """
    This method parses the environment variables injected via SCv1.
    """
    # TODO: Once support for SCv1 is deprecated, we should remove this method and rely
    # purely on settings coming via the `model-settings.json` file.
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


def load_pipeline_from_settings(
    hf_settings: HuggingFaceSettings, settings: ModelSettings
) -> Pipeline:
    # TODO: Support URI for locally downloaded artifacts
    # uri = model_parameters.uri
    pipeline = _get_pipeline_class(hf_settings)
    batch_size = 1 if settings.max_batch_size == 0 else settings.max_batch_size
    hf_pipeline = pipeline(
        hf_settings.task_name,
        model=hf_settings.pretrained_model,
        tokenizer=hf_settings.tokenizer or hf_settings.pretrained_model,
        device=hf_settings.device,
        batch_size=batch_size,
        framework=hf_settings.framework,
    )

    # If max_batch_size > 0 we need to ensure tokens are padded
    if settings.max_batch_size:
        hf_pipeline.tokenizer.pad_token_id = [str(pp.model.config.eos_token_id)]  # type: ignore

    return hf_pipeline


def _get_pipeline_class(hf_settings: HuggingfaceSettings) -> _PipelineConstructor:
    if hf_settings.optimum_model:
        return partial(opt_pipeline, accelerator=OPTIMUM_ACCELERATOR)

    return trf_pipeline


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
