from enum import Enum
from importlib import import_module

from pydantic import BaseSettings

from .openai.common import OpenAISettings

ENV_PREFIX_LLM_SETTINGS = "MLSERVER_MODEL_LLM_"
PROVIDER_ID_TAG = "provider_id"


class LLMProviderList(str, Enum):
    openai = "openai"


class LLMBaseSettings(BaseSettings):
    """
    LLM base settings
    """
    class Config:
        env_prefix = ENV_PREFIX_LLM_SETTINGS

    provider_id: LLMProviderList
    config: OpenAISettings


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1:])
    return klass
