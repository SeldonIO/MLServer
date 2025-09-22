# Module `mlserver.registry`


## Class `MultiModelRegistry`


**Description:**
Multiple model registry, where each model can have multiple versions.

### Method `get_model`


**Signature:** `get_model(self, name: str, version: Optional[str] = None) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `get_models`


**Signature:** `get_models(self, name: Optional[str] = None) -> List[mlserver.model.MLModel]`


**Description:**
*No docstring available.*

### Method `load`


**Signature:** `load(self, model_settings: mlserver.settings.ModelSettings) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `unload`


**Signature:** `unload(self, name: str)`


**Description:**
*No docstring available.*

### Method `unload_version`


**Signature:** `unload_version(self, name: str, version: Optional[str] = None)`


**Description:**
*No docstring available.*

## Class `SingleModelRegistry`


**Description:**
Registry for a single model with multiple versions.

### Method `empty`


**Signature:** `empty(self) -> bool`


**Description:**
*No docstring available.*

### Method `get_model`


**Signature:** `get_model(self, version: Optional[str] = None) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `get_models`


**Signature:** `get_models(self) -> List[mlserver.model.MLModel]`


**Description:**
*No docstring available.*

### Method `load`


**Signature:** `load(self, model_settings: mlserver.settings.ModelSettings) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `unload`


**Signature:** `unload(self)`


**Description:**
*No docstring available.*

### Method `unload_version`


**Signature:** `unload_version(self, version: Optional[str] = None)`


**Description:**
*No docstring available.*

## Function `model_initialiser`


**Signature:** `model_initialiser(model_settings: mlserver.settings.ModelSettings) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*
