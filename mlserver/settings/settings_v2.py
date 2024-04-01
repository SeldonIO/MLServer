from pydantic import Field

from mlserver.settings.commons import _ModelSettings


class ModelSettings(_ModelSettings):

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
