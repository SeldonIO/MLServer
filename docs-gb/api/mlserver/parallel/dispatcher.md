# Module `mlserver.parallel.dispatcher`


## Class `AsyncResponses`


**Description:**
*No docstring available.*

### Method `cancel`


**Signature:** `cancel(self, worker: mlserver.parallel.worker.Worker, exit_code: int)`


**Description:**
Cancel in-flight requests for worker (e.g. because it died
unexpectedly).

### Method `resolve`


**Signature:** `resolve(self, response: mlserver.parallel.messages.ModelResponseMessage)`


**Description:**
Resolve a previously scheduled response future.

### Method `schedule_and_wait`


**Signature:** `schedule_and_wait(self, message: mlserver.parallel.messages.Message, worker: mlserver.parallel.worker.Worker) -> mlserver.parallel.messages.ModelResponseMessage`


**Description:**
Schedule a response and wait until it gets resolved.

## Class `Dispatcher`


**Description:**
*No docstring available.*

### Method `dispatch_request`


**Signature:** `dispatch_request(self, request_message: mlserver.parallel.messages.ModelRequestMessage) -> mlserver.parallel.messages.ModelResponseMessage`


**Description:**
*No docstring available.*

### Method `dispatch_update`


**Signature:** `dispatch_update(self, model_update: mlserver.parallel.messages.ModelUpdateMessage) -> List[mlserver.parallel.messages.ModelResponseMessage]`


**Description:**
*No docstring available.*

### Method `dispatch_update_to_worker`


**Signature:** `dispatch_update_to_worker(self, worker: mlserver.parallel.worker.Worker, model_update: mlserver.parallel.messages.ModelUpdateMessage) -> mlserver.parallel.messages.ModelResponseMessage`


**Description:**
*No docstring available.*

### Method `on_worker_ready`


**Signature:** `on_worker_ready(self, worker: mlserver.parallel.worker.Worker)`


**Description:**
Handler for workers who are now ready to receive traffic.

### Method `on_worker_start`


**Signature:** `on_worker_start(self, worker: mlserver.parallel.worker.Worker)`


**Description:**
Handler for workers who have just started but are still not ready to
receive traffic.
This is used for workers that got restarted and need to reload all
models.

### Method `on_worker_stop`


**Signature:** `on_worker_stop(self, worker: mlserver.parallel.worker.Worker, exit_code: int)`


**Description:**
Handler used for workers who stopped unexpectedly and there need to be
removed from the round robin rotation.

### Method `start`


**Signature:** `start(self)`


**Description:**
*No docstring available.*

### Method `stop`


**Signature:** `stop(self)`


**Description:**
*No docstring available.*
