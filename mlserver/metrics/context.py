from prometheus_client import Histogram

from .registry import REGISTRY


SELDON_MODEL_NAME_LABEL = "model_name"
SELDON_MODEL_VERSION_LABEL = "model_version"


def _get_or_create(metric_name: str) -> Histogram:
    if metric_name in REGISTRY:
        # TODO: Check if metric is a Histogram?
        return REGISTRY[metric_name]

    return Histogram(metric_name, "TOOD: Description??", registry=REGISTRY)


def log(**metrics):
    for metric_name, metric_value in metrics.items():
        metric = _get_or_create(metric_name)
        metric.observe(metric_value)
