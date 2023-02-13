from prometheus_client import REGISTRY
from prometheus_client.multiprocess import MultiProcessCollector

from mlserver.settings import Settings

from mlserver.metrics.prometheus import PrometheusEndpoint


def test_get_registry(prometheus_endpoint: PrometheusEndpoint, settings: Settings):
    collectors = [c for c in prometheus_endpoint._registry._collector_to_names.keys()]

    assert len(collectors) == 1
    assert isinstance(collectors[0], MultiProcessCollector)
    assert collectors[0]._path == settings.metrics_dir


def test_get_registry_no_parallel(settings: Settings):
    settings.parallel_workers = 0
    endpoint = PrometheusEndpoint(settings)

    assert endpoint._registry == REGISTRY
