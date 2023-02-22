import pytest

from prometheus_client import Histogram

from mlserver.metrics.registry import MetricsRegistry


@pytest.fixture
def registry() -> MetricsRegistry:
    return MetricsRegistry()


@pytest.fixture
def metric(registry: MetricsRegistry) -> Histogram:
    return Histogram("foo", "bar bar2 bar3", registry=registry)


@pytest.mark.parametrize(
    "metric_name, expected", [("foo", True), ("something_else", False)]
)
def test_exists(
    registry: MetricsRegistry, metric: Histogram, metric_name: str, expected: bool
):
    assert registry.exists(metric_name) == expected


def test_get(registry: MetricsRegistry, metric: Histogram):
    assert registry.get(metric._name) == metric


def test_get_error(registry: MetricsRegistry, metric: Histogram):
    with pytest.raises(KeyError):
        registry.get("something_else")
