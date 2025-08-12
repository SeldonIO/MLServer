# mlserver.metrics

### *class* mlserver.metrics.MetricsServer(settings: Settings)

Bases: `object`

#### *async* on_worker_stop(worker: Worker)

#### *async* start()

#### *async* stop(sig: int | None = None)

### mlserver.metrics.configure_metrics(settings: Settings)

### mlserver.metrics.register(name: str, description: str)

Registers a new metric with its description.
If the metric already exists, it will just return the existing one.

### mlserver.metrics.log(\*\*metrics)

Logs a new set of metric values.
Each kwarg of this method will be treated as a separate metric / value
pair.
If any of the metrics does not exist, a new one will be created with a
default description.
