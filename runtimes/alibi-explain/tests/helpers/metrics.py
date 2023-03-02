from prometheus_client import CollectorRegistry


def unregister_metrics(registry: CollectorRegistry):
    # NOTE: Since `REGISTRY` objects are usually global, this method is NOT
    # thread-safe!!
    collectors = list(registry._collector_to_names.keys())
    for collector in collectors:
        registry.unregister(collector)
