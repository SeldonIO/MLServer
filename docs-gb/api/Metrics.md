# Metrics

## MetricsServer

### Methods

### on_worker_stop()

```python
on_worker_stop(self, worker: Worker) -> None
```

_No description available._

### start()

```python
start(self)
```

_No description available._

### stop()

```python
stop(self, sig: Optional[int] = None)
```

_No description available._

## configure_metrics()

```python
configure_metrics(settings: Settings)
```

_No description available._

## log()

```python
log(metrics)
```

Logs a new set of metric values.
Each kwarg of this method will be treated as a separate metric / value
pair.
If any of the metrics does not exist, a new one will be created with a
default description.

## register()

```python
register(name: str, description: str) -> Histogram
```

Registers a new metric with its description.
If the metric already exists, it will just return the existing one.

