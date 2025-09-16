# Module `mlserver.handlers.dataplane`


## Class `DataPlane`


**Description:**
Internal implementation of handlers, used by both the gRPC and REST
servers.

### Method `infer`


**Signature:** `infer(self, payload: mlserver.types.dataplane.InferenceRequest, name: str, version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
*No docstring available.*

### Method `infer_stream`


**Signature:** `infer_stream(self, payloads: AsyncIterator[mlserver.types.dataplane.InferenceRequest], name: str, version: Optional[str] = None) -> AsyncIterator[mlserver.types.dataplane.InferenceResponse]`


**Description:**
*No docstring available.*

### Method `live`


**Signature:** `live(self) -> bool`


**Description:**
*No docstring available.*

### Method `metadata`


**Signature:** `metadata(self) -> mlserver.types.dataplane.MetadataServerResponse`


**Description:**
*No docstring available.*

### Method `model_metadata`


**Signature:** `model_metadata(self, name: str, version: Optional[str] = None) -> mlserver.types.dataplane.MetadataModelResponse`


**Description:**
*No docstring available.*

### Method `model_ready`


**Signature:** `model_ready(self, name: str, version: Optional[str] = None) -> bool`


**Description:**
*No docstring available.*

### Method `ready`


**Signature:** `ready(self) -> bool`


**Description:**
*No docstring available.*
