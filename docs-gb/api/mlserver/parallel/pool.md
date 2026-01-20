# Module `mlserver.parallel.pool`


## Class `InferencePool`


**Description:**
The InferencePool class represents a pool of workers where we can run
inference on.

Under the hood, it's responsible for managing a pool of multiprocessing
workers, where the model is loaded.
This approach lets MLServer work around the GIL to make sure that inference
can occur in parallel across multiple models or instances of a model.

### Method `close`


**Signature:** `close(self)`


**Description:**
*No docstring available.*

### Method `empty`


**Signature:** `empty(self) -> bool`


**Description:**
*No docstring available.*

### Method `load_model`


**Signature:** `load_model(self, model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `on_worker_stop`


**Signature:** `on_worker_stop(self, pid: int, exit_code: int)`


**Description:**
*No docstring available.*

### Method `reload_model`


**Signature:** `reload_model(self, old_model: mlserver.model.MLModel, new_model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `unload_model`


**Signature:** `unload_model(self, model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

## Class `WorkerRegistry`


**Description:**
Simple registry to keep track of which models have been loaded.
This can be used to re-load all models when a worker stops unexpectedly.

### Method `add`


**Signature:** `add(self, model_settings: mlserver.settings.ModelSettings)`


**Description:**
*No docstring available.*

### Method `remove`


**Signature:** `remove(self, model_settings: mlserver.settings.ModelSettings)`


**Description:**
*No docstring available.*
