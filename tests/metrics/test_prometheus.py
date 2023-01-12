from prometheus_client import REGISTRY
from prometheus_client.multiprocess import MultiProcessCollector

from mlserver.settings import Settings

from mlserver.metrics.prometheus import get_registry


def test_get_registry(settings: Settings):
    registry = get_registry(settings)
    collectors = [c for c in registry._collector_to_names.keys()]

    assert len(collectors) == 1
    assert isinstance(collectors[0], MultiProcessCollector)
    assert collectors[0]._path == settings.metrics_dir


def test_get_registry_no_parallel(settings: Settings):
    settings.parallel_workers = 0
    registry = get_registry(settings)

    assert registry == REGISTRY
