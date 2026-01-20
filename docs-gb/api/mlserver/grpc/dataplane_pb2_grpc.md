# Module `mlserver.grpc.dataplane_pb2_grpc`


## Class `GRPCInferenceService`


**Description:**
Inference Server GRPC endpoints.

### Method `ModelInfer`


**Signature:** `ModelInfer(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `ModelMetadata`


**Signature:** `ModelMetadata(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `ModelReady`


**Signature:** `ModelReady(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `ModelStreamInfer`


**Signature:** `ModelStreamInfer(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `RepositoryIndex`


**Signature:** `RepositoryIndex(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `RepositoryModelLoad`


**Signature:** `RepositoryModelLoad(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `RepositoryModelUnload`


**Signature:** `RepositoryModelUnload(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `ServerLive`


**Signature:** `ServerLive(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `ServerMetadata`


**Signature:** `ServerMetadata(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

### Method `ServerReady`


**Signature:** `ServerReady(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)`


**Description:**
*No docstring available.*

## Class `GRPCInferenceServiceServicer`


**Description:**
Inference Server GRPC endpoints.

### Method `ModelInfer`


**Signature:** `ModelInfer(self, request, context)`


**Description:**
Perform inference using a specific model.

### Method `ModelMetadata`


**Signature:** `ModelMetadata(self, request, context)`


**Description:**
Get model metadata.

### Method `ModelReady`


**Signature:** `ModelReady(self, request, context)`


**Description:**
Check readiness of a model in the inference server.

### Method `ModelStreamInfer`


**Signature:** `ModelStreamInfer(self, request_iterator, context)`


**Description:**
Perform stream inference using a specific model.

### Method `RepositoryIndex`


**Signature:** `RepositoryIndex(self, request, context)`


**Description:**
Get the index of model repository contents.

### Method `RepositoryModelLoad`


**Signature:** `RepositoryModelLoad(self, request, context)`


**Description:**
Load or reload a model from a repository.

### Method `RepositoryModelUnload`


**Signature:** `RepositoryModelUnload(self, request, context)`


**Description:**
Unload a model.

### Method `ServerLive`


**Signature:** `ServerLive(self, request, context)`


**Description:**
Check liveness of the inference server.

### Method `ServerMetadata`


**Signature:** `ServerMetadata(self, request, context)`


**Description:**
Get server metadata.

### Method `ServerReady`


**Signature:** `ServerReady(self, request, context)`


**Description:**
Check readiness of the inference server.

## Class `GRPCInferenceServiceStub`


**Description:**
Inference Server GRPC endpoints.

## Function `add_GRPCInferenceServiceServicer_to_server`


**Signature:** `add_GRPCInferenceServiceServicer_to_server(servicer, server)`


**Description:**
*No docstring available.*
