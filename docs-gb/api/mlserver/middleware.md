# Module `mlserver.middleware`


## Class `InferenceMiddleware`


**Description:**
Base class to implement middlewares.

### Method `request_middleware`


**Signature:** `request_middleware(self, request: mlserver.types.dataplane.InferenceRequest, model_settings: mlserver.settings.ModelSettings) -> mlserver.types.dataplane.InferenceRequest`


**Description:**
*No docstring available.*

### Method `response_middleware`


**Signature:** `response_middleware(self, response: mlserver.types.dataplane.InferenceResponse, model_settings: mlserver.settings.ModelSettings) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
*No docstring available.*

## Class `InferenceMiddlewares`


**Description:**
Meta-middleware which applies a list of middlewares.

### Method `request_middleware`


**Signature:** `request_middleware(self, request: mlserver.types.dataplane.InferenceRequest, model_settings: mlserver.settings.ModelSettings) -> mlserver.types.dataplane.InferenceRequest`


**Description:**
*No docstring available.*

### Method `response_middleware`


**Signature:** `response_middleware(self, response: mlserver.types.dataplane.InferenceResponse, model_settings: mlserver.settings.ModelSettings) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
*No docstring available.*
