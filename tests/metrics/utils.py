from typing import List, Optional

from prometheus_client import Metric, CollectorRegistry
from prometheus_client.parser import text_string_to_metric_families

from ..utils import RESTClient


class MetricsClient(RESTClient):
    def __init__(self, *args, metrics_endpoint: str = "/metrics", **kwargs):
        super().__init__(*args, **kwargs)
        self._metrics_endpoint = metrics_endpoint

    async def wait_until_ready(self) -> None:
        endpoint = f"http://{self._http_server}{self._metrics_endpoint}"
        await self._retry_get(endpoint)

    async def metrics(self) -> List[Metric]:
        endpoint = f"http://{self._http_server}{self._metrics_endpoint}"
        response = await self._session.get(endpoint)

        raw_metrics = await response.text()
        return text_string_to_metric_families(raw_metrics)


def find_metric(metrics: List[Metric], name: str) -> Optional[Metric]:
    for metric in metrics:
        if metric.name == name:
            return metric

    return None


def unregister_metrics(registry: CollectorRegistry):
    # NOTE: Since `REGISTRY` objects are usually global, this method is NOT
    # thread-safe!!
    collectors = list(registry._collector_to_names.keys())
    for collector in collectors:
        registry.unregister(collector)
