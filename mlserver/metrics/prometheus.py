import os

from prometheus_client import REGISTRY, CollectorRegistry
from prometheus_client.multiprocess import MultiProcessCollector

from ..settings import Settings


def get_registry(settings: Settings) -> CollectorRegistry:
    if not settings.parallel_workers:
        return REGISTRY

    if not settings.metrics_dir:
        settings.metrics_dir = os.getcwd()

    registry = CollectorRegistry()
    MultiProcessCollector(registry, path=settings.metrics_dir)

    return registry
