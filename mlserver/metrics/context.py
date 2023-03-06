from contextvars import ContextVar
from contextlib import contextmanager
from prometheus_client import Histogram

from ..settings import ModelSettings
from .registry import REGISTRY
from .errors import InvalidModelContext

model_name_var: ContextVar[str] = ContextVar("model_name")
model_version_var: ContextVar[str] = ContextVar("model_version")

SELDON_MODEL_NAME_LABEL = "model_name"
SELDON_MODEL_VERSION_LABEL = "model_version"


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


def register(name: str, description: str) -> Histogram:
    """
    Registers a new metric with its description.
    If the metric already exists, it will just return the existing one.
    """
    if name in REGISTRY:
        # TODO: Check if metric is a Histogram?
        return REGISTRY[name]  # type: ignore

    # TODO: How to enable multiple metric types?
    return Histogram(
        name,
        description,
        labelnames=[SELDON_MODEL_NAME_LABEL, SELDON_MODEL_VERSION_LABEL],
        registry=REGISTRY,
    )


def _get_labels_from_context() -> dict:
    try:
        model_name = model_name_var.get()
        model_version = model_version_var.get()
        return {
            SELDON_MODEL_NAME_LABEL: model_name,
            SELDON_MODEL_VERSION_LABEL: model_version,
        }
    except LookupError:
        raise InvalidModelContext()


def log(**metrics):
    """
    Logs a new set of metric values.
    Each kwarg of this method will be treated as a separate metric / value
    pair.
    If any of the metrics does not exist, a new one will be created with a
    default description.
    """
    labels = _get_labels_from_context()
    for metric_name, metric_value in metrics.items():
        metric = register(metric_name, "TODO: Default description?")
        with_labels = metric.labels(**labels)
        with_labels.observe(metric_value, labels)
