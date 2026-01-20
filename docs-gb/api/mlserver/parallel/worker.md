# Module `mlserver.parallel.worker`


## Class `Worker`


**Description:**
Process objects represent activity that is run in a separate process
The class is analogous to `threading.Thread`

### Method `close`


**Signature:** `close(self)`


**Description:**
Close the Process object.
This method releases resources held by the Process object.  It is
an error to call this method if the child process is still running.

### Method `coro_run`


**Signature:** `coro_run(self)`


**Description:**
*No docstring available.*

### Method `is_alive`


**Signature:** `is_alive(self)`


**Description:**
Return whether process is alive

### Method `join`


**Signature:** `join(self, timeout=None)`


**Description:**
Wait until child process terminates

### Method `kill`


**Signature:** `kill(self)`


**Description:**
Terminate process; sends SIGKILL signal or uses TerminateProcess()

### Method `run`


**Signature:** `run(self)`


**Description:**
Method to be run in sub-process; can be overridden in sub-class

### Method `send_request`


**Signature:** `send_request(self, request_message: mlserver.parallel.messages.ModelRequestMessage)`


**Description:**
Send an inference request message to the worker.
Note that this method should be both multiprocess- and thread-safe.

### Method `send_update`


**Signature:** `send_update(self, model_update: mlserver.parallel.messages.ModelUpdateMessage)`


**Description:**
Send a model update to the worker.
Note that this method should be both multiprocess- and thread-safe.

### Method `start`


**Signature:** `start(self)`


**Description:**
Start child process

### Method `stop`


**Signature:** `stop(self)`


**Description:**
Close the worker's main loop.
Note that this method should be both multiprocess- and thread-safe.

### Method `terminate`


**Signature:** `terminate(self)`


**Description:**
Terminate process; sends SIGTERM signal or uses TerminateProcess()
