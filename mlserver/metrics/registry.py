from prometheus_client import CollectorRegistry
from prometheus_client.metrics import MetricWrapperBase


class MetricsRegistry(CollectorRegistry):
    """
    Keep track of registered metrics to allow reusing them.
    """

    def exists(self, metric_name: str) -> bool:
        return metric_name in self._names_to_collectors

    def get(self, metric_name: str) -> MetricWrapperBase:
        # TODO: Check that it's a MetricWrapperBase?
        return self._names_to_collectors[metric_name]

    def __getitem__(self, metric_name: str) -> MetricWrapperBase:
        return self.get(metric_name)

    def __contains__(self, metric_name: str) -> bool:
        return self.exists(metric_name)


REGISTRY = MetricsRegistry()
