from mlserver.errors import MLServerError
from transformers.pipelines import SUPPORTED_TASKS

from .common import SUPPORTED_OPTIMUM_TASKS


class MissingHuggingFaceSettings(MLServerError):
    def __init__(self):
        super().__init__("Missing HuggingFace Runtime settings.")


class InvalidHuggingFaceTask(MLServerError):
    def __init__(self, task: str):
        msg = (
            f"Invalid transformer task: {task}."
            f" Available tasks: {SUPPORTED_TASKS.keys()}"
        )
        super().__init__(msg)


class InvalidOptimumTask(MLServerError):
    def __init__(self, task: str):
        msg = (
            "Invalid transformer task for Optimum model: {task}. "
            f"Supported Optimum tasks: {SUPPORTED_OPTIMUM_TASKS.keys()}"
        )
        super().__init__(msg)


class InvalidModelParameter(MLServerError):
    def __init__(self, name: str, value: str, param_type: str):
        msg = (
            f"Bad model parameter: {name}"
            f" with value {value}"
            f" can't be parsed as a {param_type}"
        )
        super().__init__(msg)


class InvalidModelParameterType(MLServerError):
    def __init__(self, param_type: str):
        msg = (
            f"Bad model parameter type: {param_type}."
            f" Only valid types are INT, FLOAT, DOUBLE, STRING, BOOL."
        )
        super().__init__(msg)
