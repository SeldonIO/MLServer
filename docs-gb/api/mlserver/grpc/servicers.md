# Module `mlserver.grpc.servicers`


## Class `InferenceServicer`


**Description:**
Inference Server GRPC endpoints.

### Method `ModelInfer`


**Signature:** `ModelInfer(self, request, context)`


**Description:**
*No docstring available.*

### Method `ModelMetadata`


**Signature:** `ModelMetadata(self, request, context)`


**Description:**
*No docstring available.*

### Method `ModelReady`


**Signature:** `ModelReady(self, request: dataplane_pb2.ModelReadyRequest, context) -> dataplane_pb2.ModelReadyResponse`


**Description:**
Check readiness of a model in the inference server.

### Method `ModelStreamInfer`


**Signature:** `ModelStreamInfer(self, request_stream, context)`


**Description:**
*No docstring available.*

### Method `RepositoryIndex`


**Signature:** `RepositoryIndex(self, request: dataplane_pb2.RepositoryIndexRequest, context) -> dataplane_pb2.RepositoryIndexResponse`


**Description:**
Get the index of model repository contents.

### Method `RepositoryModelLoad`


**Signature:** `RepositoryModelLoad(self, request, context)`


**Description:**
*No docstring available.*

### Method `RepositoryModelUnload`


**Signature:** `RepositoryModelUnload(self, request, context)`


**Description:**
*No docstring available.*

### Method `ServerLive`


**Signature:** `ServerLive(self, request: dataplane_pb2.ServerLiveRequest, context) -> dataplane_pb2.ServerLiveResponse`


**Description:**
Check liveness of the inference server.

### Method `ServerMetadata`


**Signature:** `ServerMetadata(self, request: dataplane_pb2.ServerMetadataRequest, context) -> dataplane_pb2.ServerMetadataResponse`


**Description:**
Get server metadata.

### Method `ServerReady`


**Signature:** `ServerReady(self, request: dataplane_pb2.ServerReadyRequest, context) -> dataplane_pb2.ServerReadyResponse`


**Description:**
Check readiness of the inference server.
