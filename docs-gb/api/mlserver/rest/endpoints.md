# Module `mlserver.rest.endpoints`


## Class `Endpoints`


**Description:**
Implementation of REST endpoints.
These take care of the REST/HTTP-specific things and then delegate the
business logic to the internal handlers.

### Method `docs`


**Signature:** `docs(self) -> starlette.responses.HTMLResponse`


**Description:**
*No docstring available.*

### Method `infer`


**Signature:** `infer(self, raw_request: starlette.requests.Request, raw_response: starlette.responses.Response, payload: mlserver.types.dataplane.InferenceRequest, model_name: str, model_version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
*No docstring available.*

### Method `infer_stream`


**Signature:** `infer_stream(self, raw_request: starlette.requests.Request, payload: mlserver.types.dataplane.InferenceRequest, model_name: str, model_version: Optional[str] = None) -> starlette.responses.StreamingResponse`


**Description:**
*No docstring available.*

### Method `live`


**Signature:** `live(self) -> starlette.responses.Response`


**Description:**
*No docstring available.*

### Method `metadata`


**Signature:** `metadata(self) -> mlserver.types.dataplane.MetadataServerResponse`


**Description:**
*No docstring available.*

### Method `model_docs`


**Signature:** `model_docs(self, model_name: str, model_version: Optional[str] = None) -> starlette.responses.HTMLResponse`


**Description:**
*No docstring available.*

### Method `model_metadata`


**Signature:** `model_metadata(self, model_name: str, model_version: Optional[str] = None) -> mlserver.types.dataplane.MetadataModelResponse`


**Description:**
*No docstring available.*

### Method `model_openapi`


**Signature:** `model_openapi(self, model_name: str, model_version: Optional[str] = None) -> dict`


**Description:**
*No docstring available.*

### Method `model_ready`


**Signature:** `model_ready(self, model_name: str, model_version: Optional[str] = None) -> starlette.responses.Response`


**Description:**
*No docstring available.*

### Method `openapi`


**Signature:** `openapi(self) -> dict`


**Description:**
*No docstring available.*

### Method `ready`


**Signature:** `ready(self) -> starlette.responses.Response`


**Description:**
*No docstring available.*

## Class `ModelRepositoryEndpoints`


**Description:**
*No docstring available.*

### Method `index`


**Signature:** `index(self, payload: mlserver.types.model_repository.RepositoryIndexRequest) -> mlserver.types.model_repository.RepositoryIndexResponse`


**Description:**
*No docstring available.*

### Method `load`


**Signature:** `load(self, model_name: str) -> starlette.responses.Response`


**Description:**
*No docstring available.*

### Method `unload`


**Signature:** `unload(self, model_name: str) -> starlette.responses.Response`


**Description:**
*No docstring available.*
