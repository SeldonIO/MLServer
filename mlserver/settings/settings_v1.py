from pydantic import Extra, Field

from mlserver.settings.commons import (
    ENV_FILE_SETTINGS,
    ENV_PREFIX_SETTINGS,
    ENV_PREFIX_MODEL_SETTINGS,
    CORSSettings,
    Settings,
    ModelParameters,
    ModelSettings as _ModelSettings,
)


class _CORSConfig:
    env_file = ENV_FILE_SETTINGS
    env_prefix = ENV_PREFIX_SETTINGS


class _SettingsConfig:
    env_file = ENV_FILE_SETTINGS
    env_prefix = ENV_PREFIX_SETTINGS


class _ModelParametersConfig:
    extra = Extra.allow
    env_file = ENV_FILE_SETTINGS
    env_prefix = ENV_PREFIX_MODEL_SETTINGS


CORSSettings.Config = _CORSConfig
Settings.Config = _SettingsConfig
ModelParameters.Config = _ModelParametersConfig


class ModelSettings(_ModelSettings):
    class Config:
        env_file = ENV_FILE_SETTINGS
        env_prefix = ENV_PREFIX_MODEL_SETTINGS
        underscore_attrs_are_private = True

    # Custom model class implementation
    # NOTE: The `implementation_` attr will only point to the string import.
    # The actual import will occur within the `implementation` property - think
    # of this as a lazy import.
    # You should always use `model_settings.implementation` and treat
    # `implementation_` as a private attr (due to Pydantic - we can't just
    # prefix the attr with `_`).
    implementation_: str = Field(
        alias="implementation", env="MLSERVER_MODEL_IMPLEMENTATION"
    )
    """*Python path* to the inference runtime to use to serve this model (e.g.
    ``mlserver_sklearn.SKLearnModel``)."""
