import os
import orjson

from typing import Optional, Dict
from pydantic import BaseSettings
from distutils.util import strtobool

from .errors import InvalidModelParameter, InvalidModelParameterType

ENV_PREFIX_HUGGINGFACE_SETTINGS = "MLSERVER_MODEL_HUGGINGFACE_"
PARAMETERS_ENV_NAME = "PREDICTIVE_UNIT_PARAMETERS"


class HuggingFaceSettings(BaseSettings):
    """
    Parameters that apply only to HuggingFace models
    """

    class Config:
        env_prefix = ENV_PREFIX_HUGGINGFACE_SETTINGS

    # TODO: Document fields
    task: str = ""
    """
    Pipeline task to load.
    You can see the available Optimum and Transformers tasks available in the
    links below:

    - `Optimum Tasks <https://huggingface.co/docs/optimum/onnxruntime/usage_guides/pipelines#inference-pipelines-with-the-onnx-runtime-accelerator>`_
    - `Transformer Tasks <https://huggingface.co/docs/transformers/task_summary>`_
    """  # noqa: E501

    task_suffix: str = ""
    """
    Suffix to append to the base task name.
    Useful for, e.g. translation tasks which require a suffix on the task name
    to specify source and target.
    """

    pretrained_model: Optional[str] = None
    """
    Name of the model that should be loaded in the pipeline.
    """

    pretrained_tokenizer: Optional[str] = None
    """
    Name of the tokenizer that should be loaded in the pipeline.
    """

    framework: Optional[str] = None
    """
    The framework to use, either "pt" for PyTorch or "tf" for TensorFlow.
    """

    optimum_model: bool = False
    """
    Flag to decide whether the pipeline should use a Optimum-optimised model or
    the standard Transformers model.
    Under the hood, this will enable the model to use the optimised ONNX
    runtime.
    """

    device: int = -1
    """
    Device in which this pipeline will be loaded (e.g., "cpu", "cuda:1", "mps",
    or a GPU ordinal rank like 1).
    """

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
    parameters = orjson.loads(os.environ.get(PARAMETERS_ENV_NAME, "[]"))

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
                raise InvalidModelParameter(name, value, type_)
            except KeyError:
                raise InvalidModelParameterType(type_)
    return parsed_parameters
