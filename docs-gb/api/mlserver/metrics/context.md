# Module `mlserver.metrics.context`


## Function `log`


**Signature:** `log(**metrics)`


**Description:**
Logs a new set of metric values.
Each kwarg of this method will be treated as a separate metric / value
pair.
If any of the metrics does not exist, a new one will be created with a
default description.

## Function `register`


**Signature:** `register(name: str, description: str) -> prometheus_client.metrics.Histogram`


**Description:**
Registers a new metric with its description.
If the metric already exists, it will just return the existing one.
