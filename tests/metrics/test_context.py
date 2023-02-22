import pytest

from prometheus_client import Histogram

from mlserver.settings import ModelSettings
from mlserver.metrics.registry import MetricsRegistry
from mlserver.metrics.context import register, log, model_context


@pytest.register
def model_context(sum_model_settings: ModelSettings):
    with model_context(sum_model_settings):
        yield


def test_register(metrics_registry: MetricsRegistry, model_context):
    register("foo", "My custom description")

    assert "foo" in metrics_registry

    metric = metrics_registry["foo"]
    assert isinstance(metric, Histogram)
    assert metric._documentation == "My custom description"


def test_log(metrics_registry: MetricsRegistry, model_context):
    log(foo=3.2)

    assert "foo" in metrics_registry

    metric = metrics_registry["foo"]
    assert isinstance(metric, Histogram)
    assert metric._sum._value == 3.2
