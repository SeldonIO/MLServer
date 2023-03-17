from enum import Enum

from pydantic import BaseSettings

from .openai.common import OpenAISettings

LLM_CALL_PARAMETERS_TAG = "llm_parameters"
_ENV_PREFIX_LLM_SETTINGS = "MLSERVER_MODEL_LLM_"
PROVIDER_ID_TAG = "provider_id"


class LLMProviderEnum(str, Enum):
    openai = "openai"


class LLMSettings(BaseSettings):
    """
    LLM base settings
    """

    class Config:
        env_prefix = _ENV_PREFIX_LLM_SETTINGS

    provider_id: LLMProviderEnum
    # this would be a Union of Settings in the future
    config: OpenAISettings
