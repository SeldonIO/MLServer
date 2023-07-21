from contextlib import contextmanager
from contextvars import ContextVar

from .settings import ModelSettings

MODEL_NAME_VAR: ContextVar[str] = ContextVar("model_name")
MODEL_VERSION_VAR: ContextVar[str] = ContextVar("model_version")


@contextmanager
def model_context(model_settings: ModelSettings):
    model_name_token = MODEL_NAME_VAR.set(model_settings.name)

    model_version = ""
    if model_settings.version:
        model_version = model_settings.version
    model_version_token = MODEL_VERSION_VAR.set(model_version)

    try:
        yield
    finally:
        MODEL_NAME_VAR.reset(model_name_token)
        MODEL_VERSION_VAR.reset(model_version_token)
