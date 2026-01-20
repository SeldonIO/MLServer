# Module `mlserver.metrics.registry`


## Class `MetricsRegistry`


**Description:**
Keep track of registered metrics to allow reusing them.

### Method `collect`


**Signature:** `collect(self) -> Iterable[prometheus_client.metrics_core.Metric]`


**Description:**
Yields metrics from the collectors in the registry.

### Method `exists`


**Signature:** `exists(self, metric_name: str) -> bool`


**Description:**
*No docstring available.*

### Method `get`


**Signature:** `get(self, metric_name: str) -> prometheus_client.metrics.MetricWrapperBase`


**Description:**
*No docstring available.*

### Method `get_sample_value`


**Signature:** `get_sample_value(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[float]`


**Description:**
Returns the sample value, or None if not found.
This is inefficient, and intended only for use in unittests.

### Method `get_target_info`


**Signature:** `get_target_info(self) -> Optional[Dict[str, str]]`


**Description:**
*No docstring available.*

### Method `register`


**Signature:** `register(self, collector: prometheus_client.registry.Collector) -> None`


**Description:**
Add a collector to the registry.

### Method `restricted_registry`


**Signature:** `restricted_registry(self, names: Iterable[str]) -> 'RestrictedRegistry'`


**Description:**
Returns object that only collects some metrics.
Returns an object which upon collect() will return
only samples with the given names.

Intended usage is:
    generate_latest(REGISTRY.restricted_registry(['a_timeseries']))

Experimental.

### Method `set_target_info`


**Signature:** `set_target_info(self, labels: Optional[Dict[str, str]]) -> None`


**Description:**
*No docstring available.*

### Method `unregister`


**Signature:** `unregister(self, collector: prometheus_client.registry.Collector) -> None`


**Description:**
Remove a collector from the registry.
