from typing import List, Optional

from prometheus_client import Metric
from prometheus_client.parser import text_string_to_metric_families

from ..utils import RESTClient


class MetricsClient(RESTClient):
    async def metrics(self) -> List[Metric]:
        endpoint = f"http://{self._http_server}/metrics"
        response = await self._session.get(endpoint)

        raw_metrics = await response.text()
        return text_string_to_metric_families(raw_metrics)


def find_metric(metrics: List[Metric], name: str) -> Optional[Metric]:
    for metric in metrics:
        if metric.name == name:
            return metric

    return None
