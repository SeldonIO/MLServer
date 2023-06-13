import pytest

from prometheus_client import Histogram

from mlserver.metrics.errors import MetricNotFound
from mlserver.metrics.registry import MetricsRegistry


@pytest.fixture
def metrics_registry() -> MetricsRegistry:
    return MetricsRegistry()


@pytest.fixture
def metric(metrics_registry: MetricsRegistry) -> Histogram:
    return Histogram("foo", "bar bar2 bar3", registry=metrics_registry)


@pytest.mark.parametrize(
    "metric_name, expected", [("foo", True), ("something_else", False)]
)
def test_exists(
    metrics_registry: MetricsRegistry,
    metric: Histogram,
    metric_name: str,
    expected: bool,
):
    assert (metric_name in metrics_registry) == expected


def test_get(metrics_registry: MetricsRegistry, metric: Histogram):
    assert metrics_registry[metric._name] == metric


def test_get_error(metrics_registry: MetricsRegistry, metric: Histogram):
    with pytest.raises(MetricNotFound):
        metrics_registry["something_else"]
