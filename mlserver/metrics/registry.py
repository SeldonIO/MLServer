from prometheus_client import CollectorRegistry
from prometheus_client.metrics import MetricWrapperBase

from .errors import MetricNotFound


class MetricsRegistry(CollectorRegistry):
    """
    Keep track of registered metrics to allow reusing them.
    """

    def exists(self, metric_name: str) -> bool:
        return metric_name in self._names_to_collectors

    def get(self, metric_name: str) -> MetricWrapperBase:
        if metric_name not in self._names_to_collectors:
            raise MetricNotFound(metric_name)

        collector = self._names_to_collectors[metric_name]
        if not isinstance(collector, MetricWrapperBase):
            raise MetricNotFound(metric_name, collector)

        return collector

    def __getitem__(self, metric_name: str) -> MetricWrapperBase:
        return self.get(metric_name)

    def __contains__(self, metric_name: str) -> bool:
        return self.exists(metric_name)


REGISTRY = MetricsRegistry(auto_describe=True)
