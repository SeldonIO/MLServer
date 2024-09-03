# Metrics

Out-of-the-box, MLServer exposes a set of metrics that help you monitor your
machine learning workloads in production.
These include standard metrics like number of requests and latency.

On top of these, you can also register and track your own [custom metrics](#custom-metrics) 
as part of your [custom inference runtimes](./custom.md).

## Default Metrics

By default, MLServer will expose metrics around inference requests (count and
error rate) and the status of its internal requests queues.
These internal queues are used for [adaptive batching](./adaptive-batching.md) and
[communication with the inference workers](./parallel-inference.md).

| Metric Name                   | Description                                                         |
| ----------------------------- | ------------------------------------------------------------------- |
| `model_infer_request_success` | Number of successful inference requests.                            |
| `model_infer_request_failure` | Number of failed inference requests.                                |
| `batch_request_queue`         | Queue size for the [adaptive batching](./adaptive-batching.md) queue.  |
| `parallel_request_queue`      | Queue size for the [inference workers](./parallel-inference.md) queue. |

### REST Server Metrics

On top of the default set of metrics, MLServer's REST server will also expose a
set of metrics specific to REST.

{% hint style="info" %}
The prefix for the REST-specific metrics will be dependent on the
`metrics_rest_server_prefix` flag from the [MLServer settings](#settings).
{% endhint %}

| Metric Name                               | Description                                                    |
| ----------------------------------------- | -------------------------------------------------------------- |
| `[rest_server]_requests`                  | Number of REST requests, labelled by endpoint and status code. |
| `[rest_server]_requests_duration_seconds` | Latency of REST requests.                                      |
| `[rest_server]_requests_in_progress`      | Number of in-flight REST requests.                             |

### gRPC Server Metrics

On top of the default set of metrics, MLServer's gRPC server will also expose a
set of metrics specific to gRPC.

| Metric Name           | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| `grpc_server_handled` | Number of gRPC requests, labelled by gRPC code and method. |
| `grpc_server_started` | Number of in-flight gRPC requests.                         |

## Custom Metrics

MLServer allows you to register custom metrics within your custom inference
runtimes.
This can be done through the `mlserver.register()` and `mlserver.log()`
methods.

- `mlserver.register`: Register a new metric.
- `mlserver.log`:
  Log a new set of metric / value pairs.
  If there's any unregistered metric, it will get registered on-the-fly.

{% hint style="info" %}
Under the hood, metrics logged through the `mlserver.log` method will get
exposed to Prometheus as a Histogram.
{% endhint %}

Custom metrics will generally be registered in the `load()
<mlserver.MLModel.load>` method and then used in the `predict()
<mlserver.MLModel.predict>` method of your [custom runtime](./custom).

```python
import mlserver

from mlserver.types import InferenceRequest, InferenceResponse

class MyCustomRuntime(mlserver.MLModel):
  async def load(self) -> bool:
    self._model = load_my_custom_model()
    mlserver.register("my_custom_metric", "This is a custom metric example")
    return True

  async def predict(self, payload: InferenceRequest) -> InferenceResponse:
    mlserver.log(my_custom_metric=34)
    # TODO: Replace for custom logic to run inference
    return self._model.predict(payload)
```

## Metrics Labelling

For metrics specific to a model (e.g. [custom metrics](#custom-metrics),
request counts, etc), MLServer will always label these with the **model name**
and **model version**.
Downstream, this will allow to aggregate and query metrics per model.

{% hint style="info" %}
If these labels are not present on a specific metric, this means that those
metrics can't be sliced at the model level.
{% endhint %}

Below, you can find the list of standardised labels that you will be able to
find on model-specific metrics:

| Label Name      | Description                         |
| --------------- | ----------------------------------- |
| `model_name`    | Model Name (e.g. `my-custom-model`) |
| `model_version` | Model Version (e.g. `v1.2.3`)       |

## Settings

MLServer will expose metric values through a metrics endpoint exposed on its
own metric server.
This endpoint can be polled by [Prometheus](https://prometheus.io/) or other
[OpenMetrics](https://openmetrics.io/)-compatible backends.

Below you can find the [settings](../reference/settings.md) available to control
the behaviour of the metrics server:

| Label Name  | Description  | Default      |
| ----------- | ------------ | ------------ |
| `metrics_endpoint` | Path under which the metrics endpoint will be exposed.  | `/metrics`  |
| `metrics_port` | Port used to serve the metrics server. | `8082` |
| `metrics_rest_server_prefix` | Prefix used for metric names specific to MLServer's REST inference interface. | `rest_server` |
| `metrics_dir`  | Directory used to store internal metric files (used to support metrics sharing across [inference workers](./parallel-inference.md)). This is equivalent to Prometheus' [`$PROMETHEUS_MULTIPROC_DIR`](https://github.com/prometheus/client_python/tree/master#multiprocess-mode-eg-gunicorn) env var. | MLServer's current working directory (i.e. `$PWD`) |
