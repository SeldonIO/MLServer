# Module `mlserver.parallel.registry`


## Class `InferencePoolRegistry`


**Description:**
Keeps track of the different inference pools loaded in the server.
Each inference pool will generally be used to load a different environment.

### Method `close`


**Signature:** `close(self)`


**Description:**
*No docstring available.*

### Method `load_model`


**Signature:** `load_model(self, model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `model_initialiser`


**Signature:** `model_initialiser(self, model_settings: mlserver.settings.ModelSettings) -> mlserver.model.MLModel`


**Description:**
Used to initialise a model object in the ModelRegistry.

### Method `reload_model`


**Signature:** `reload_model(self, old_model: mlserver.model.MLModel, new_model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

### Method `unload_model`


**Signature:** `unload_model(self, model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*
