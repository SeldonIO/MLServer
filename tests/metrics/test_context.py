import pytest

from prometheus_client import Histogram

from mlserver.metrics.registry import MetricsRegistry
from mlserver.metrics.context import log


def test_log(metrics_registry: MetricsRegistry):
    log(foo=3.2)

    assert "foo" in metrics_registry

    metric = metrics_registry["foo"]
    assert isinstance(metric, Histogram)
    assert metric._sum._value == 3.2
