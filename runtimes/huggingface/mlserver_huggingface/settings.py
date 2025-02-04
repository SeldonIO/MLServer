import os
import orjson

from typing import Optional, Dict, Union, NewType

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from distutils.util import strtobool
from transformers.pipelines import SUPPORTED_TASKS

try:
    # Optimum 1.7 changed the import name from `SUPPORTED_TASKS` to
    # `ORT_SUPPORTED_TASKS`.
    # We'll try to import the more recent one, falling back to the previous
    # import name if not present.
    # https://github.com/huggingface/optimum/blob/987b02e4f6e2a1c9325b364ff764da2e57e89902/optimum/pipelines/__init__.py#L18
    from optimum.pipelines import ORT_SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS
except ImportError:
    from optimum.pipelines import SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS

from mlserver.settings import ModelSettings

from .errors import (
    MissingHuggingFaceSettings,
    InvalidTransformersTask,
    InvalidOptimumTask,
    InvalidModelParameter,
    InvalidModelParameterType,
)

ENV_PREFIX_HUGGINGFACE_SETTINGS = "MLSERVER_MODEL_HUGGINGFACE_"
PARAMETERS_ENV_NAME = "PREDICTIVE_UNIT_PARAMETERS"


class HuggingFaceSettings(BaseSettings):
    """
    Parameters that apply only to HuggingFace models
    """

    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX_HUGGINGFACE_SETTINGS,
        extra="ignore",
        protected_namespaces=(),
    )

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
    model_kwargs: Optional[dict] = None

    @model_validator(mode='after')
    def set_default_model_kwargs(self) -> 'HuggingFaceSettings':
        self.model_kwargs = self.model_kwargs if self.model_kwargs is not None else {}
        self.model_kwargs.setdefault("torch_dtype", "auto")
        return self
    """
    model kwargs that should be loaded in the pipeline.
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

    device: Optional[Union[int, str]] = None
    """
    Device in which this pipeline will be loaded (e.g., "cpu", "cuda:1", "mps",
    or a GPU ordinal rank like 1). Default value of None becomes cpu.
    """

    inter_op_threads: Optional[int] = None
    """
    Threads used for parallelism between independent operations.
    PyTorch:
    https://pytorch.org/docs/stable/notes/cpu_threading_torchscript_inference.html
    Tensorflow:
    https://www.tensorflow.org/api_docs/python/tf/config/threading/set_inter_op_parallelism_threads
    """

    intra_op_threads: Optional[int] = None
    """
    Threads used within an individual op for parallelism.
    PyTorch:
    https://pytorch.org/docs/stable/notes/cpu_threading_torchscript_inference.html
    Tensorflow:
    https://www.tensorflow.org/api_docs/python/tf/config/threading/set_intra_op_parallelism_threads
    """

    @property
    def task_name(self):
        if self.task == "translation":
            return f"{self.task}{self.task_suffix}"
        return self.task


EXTRA_TYPE_DICT = {
    "INT": int,
    "FLOAT": float,
    "DOUBLE": float,
    "STRING": str,
    "BOOL": bool,
}

ExtraDict = NewType("ExtraDict", Dict[str, Union[str, bool, float, int]])


def parse_parameters_from_env() -> ExtraDict:
    """
    This method parses the environment variables injected via SCv1.

    At least an empty dict is always returned.
    """
    # TODO: Once support for SCv1 is deprecated, we should remove this method and rely
    # purely on settings coming via the `model-settings.json` file.
    parameters = orjson.loads(os.environ.get(PARAMETERS_ENV_NAME, "[]"))

    parsed_parameters: ExtraDict = ExtraDict({})

    # Guard: Exit early if there's no parameters
    if len(parameters) == 0:
        return parsed_parameters

    for param in parameters:
        name = param.get("name")
        value = param.get("value")
        type_ = param.get("type")
        if type_ == "BOOL":
            parsed_parameters[name] = bool(strtobool(value))
        else:
            try:
                parsed_parameters[name] = EXTRA_TYPE_DICT[type_](value)
            except ValueError:
                raise InvalidModelParameter(name, value, type_)
            except KeyError:
                raise InvalidModelParameterType(type_)

    return parsed_parameters


def get_huggingface_settings(model_settings: ModelSettings) -> HuggingFaceSettings:
    """Get the HuggingFace settings provided to the runtime"""

    env_params = parse_parameters_from_env()
    extra = merge_huggingface_settings_extra(model_settings, env_params)
    hf_settings = HuggingFaceSettings(**extra)  # type: ignore

    if hf_settings.task not in SUPPORTED_TASKS:
        raise InvalidTransformersTask(hf_settings.task, SUPPORTED_TASKS.keys())

    if hf_settings.optimum_model:
        if hf_settings.task not in SUPPORTED_OPTIMUM_TASKS:
            raise InvalidOptimumTask(hf_settings.task, SUPPORTED_OPTIMUM_TASKS.keys())

    return hf_settings


def merge_huggingface_settings_extra(
    model_settings: ModelSettings, env_params: ExtraDict
) -> ExtraDict:
    """
    This function returns the Extra field of the Settings.

    It merges them, iff they're both present, from the
    environment AND model settings file. Precedence is
    giving to the environment.
    """

    # Both `parameters` and `extra` are Optional, so we
    # need to get the value, or nothing.
    settings_params = (
        model_settings.parameters.extra
        if model_settings.parameters is not None
        else None
    )

    if settings_params is None and env_params == {}:
        # There must be settings provided by at least the environment OR model settings
        raise MissingHuggingFaceSettings()

    # Set the default value
    settings_params = settings_params or {}

    # Overwrite any conflicting keys, giving precedence to the environment
    settings_params.update(env_params)

    return ExtraDict(settings_params)
