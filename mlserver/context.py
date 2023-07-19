from contextlib import contextmanager
from contextvars import ContextVar

from .settings import ModelSettings

model_name_var: ContextVar[str] = ContextVar("model_name")
model_version_var: ContextVar[str] = ContextVar("model_version")


@contextmanager
def model_context(model_settings: ModelSettings):
    model_name_token = model_name_var.set(model_settings.name)

    model_version = ""
    if model_settings.version:
        model_version = model_settings.version
    model_version_token = model_version_var.set(model_version)

    try:
        yield
    finally:
        model_name_var.reset(model_name_token)
        model_version_var.reset(model_version_token)
