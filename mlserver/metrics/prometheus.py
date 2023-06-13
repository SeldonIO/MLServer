import glob
import os
import asyncio

from aiofiles.os import remove
from prometheus_client import (
    REGISTRY,
    CollectorRegistry,
    generate_latest,
    CONTENT_TYPE_LATEST,
    values,
)
from prometheus_client.multiprocess import MultiProcessCollector, mark_process_dead
from fastapi import Request, Response, status

from ..settings import Settings

PROMETHEUS_MULTIPROC_DIR = "PROMETHEUS_MULTIPROC_DIR"


def configure_metrics(settings: Settings):
    if not settings.parallel_workers:
        return

    # Re-set Prometheus' Value class to use the multiproc version.
    # Note that this workaround depends on initialising all metrics in a
    # lazy manner (i.e. not as global values)
    # https://github.com/prometheus/client_python/blob/781e3e1851d80a53732bb8102d5754cf9d68b3c1/prometheus_client/values.py#L126-L134
    os.makedirs(settings.metrics_dir, exist_ok=True)
    os.environ[PROMETHEUS_MULTIPROC_DIR] = settings.metrics_dir
    values.ValueClass = values.get_value_class()


async def stop_metrics(settings: Settings, pid: int):
    if not settings.parallel_workers:
        return

    mark_process_dead(pid)
    pattern = os.path.join(settings.metrics_dir, f"*_{pid}.db")
    matching_files = glob.glob(pattern)
    await asyncio.gather(*[remove(f) for f in matching_files])


class PrometheusEndpoint:
    def __init__(self, settings: Settings):
        self._settings = settings
        configure_metrics(self._settings)

    @property
    def _registry(self) -> CollectorRegistry:
        if not self._settings.parallel_workers:
            return REGISTRY

        registry = CollectorRegistry()
        MultiProcessCollector(registry)

        return registry

    def handle_metrics(self, req: Request) -> Response:
        headers = {"Content-Type": CONTENT_TYPE_LATEST}
        return Response(
            generate_latest(self._registry),
            status_code=status.HTTP_200_OK,
            headers=headers,
        )
