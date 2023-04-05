import os
import orjson

from typing import Optional, Dict
from pydantic import BaseSettings
from distutils.util import strtobool

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
