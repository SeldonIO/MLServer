from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mlserver.settings.commons import (
    ENV_FILE_SETTINGS,
    ENV_PREFIX_SETTINGS,
    ENV_PREFIX_MODEL_SETTINGS,
    CORSSettings,
    Settings,
    ModelParameters,
    ModelSettings as _ModelSettings,
)


CORSSettings.model_config = SettingsConfigDict(
    env_file=ENV_FILE_SETTINGS,
    env_prefix=ENV_PREFIX_SETTINGS,
)

Settings.model_config = SettingsConfigDict(
    env_file=ENV_FILE_SETTINGS,
    env_prefix=ENV_PREFIX_SETTINGS,
)
ModelParameters.model_config = model_config = SettingsConfigDict(
    extra="allow",
    env_file=ENV_FILE_SETTINGS,
    env_prefix=ENV_PREFIX_MODEL_SETTINGS,
)


class ModelSettings(_ModelSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_SETTINGS,
        env_prefix=ENV_PREFIX_MODEL_SETTINGS,
    )

    # Custom model class implementation
    # NOTE: The `implementation_` attr will only point to the string import.
    # The actual import will occur within the `implementation` property - think
    # of this as a lazy import.
    # You should always use `model_settings.implementation` and treat
    # `implementation_` as a private attr (due to Pydantic - we can't just
    # prefix the attr with `_`).
    implementation_: str = Field(
        alias="implementation", validation_alias="MLSERVER_MODEL_IMPLEMENTATION"
    )
    """*Python path* to the inference runtime to use to serve this model (e.g.
    ``mlserver_sklearn.SKLearnModel``)."""
