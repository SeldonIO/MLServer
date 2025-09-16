# Metrics

## Module `mlserver.metrics`

### Class `MetricsServer`

```python
class MetricsServer
```




### Function `configure_metrics`

```python
configure_metrics(settings: mlserver.settings.Settings)
```




### Function `log`

```python
log(**metrics)
```

Logs a new set of metric values.
Each kwarg of this method will be treated as a separate metric / value
pair.
If any of the metrics does not exist, a new one will be created with a
default description.


### Function `register`

```python
register(name: str, description: str) -> prometheus_client.metrics.Histogram
```

Registers a new metric with its description.
If the metric already exists, it will just return the existing one.

