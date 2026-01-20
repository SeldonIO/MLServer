# Module `mlserver.model`


## Class `MLModel`


**Description:**
Abstract inference runtime which exposes the main interface to interact
with ML models.

### Method `decode`


**Signature:** `decode(self, request_input: mlserver.types.dataplane.RequestInput, default_codec: Union[Type[ForwardRef('InputCodec')], ForwardRef('InputCodec'), NoneType] = None) -> Any`


**Description:**
Helper to decode a **request input** into its corresponding high-level
Python object.
This method will find the most appropiate :doc:`input codec
</user-guide/content-type>` based on the model's metadata and the
input's content type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### Method `decode_request`


**Signature:** `decode_request(self, inference_request: mlserver.types.dataplane.InferenceRequest, default_codec: Union[Type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec'), NoneType] = None) -> Any`


**Description:**
Helper to decode an **inference request** into its corresponding
high-level Python object.
This method will find the most appropiate :doc:`request codec
</user-guide/content-type>` based on the model's metadata and the
requests's content type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### Method `encode`


**Signature:** `encode(self, payload: Any, request_output: mlserver.types.dataplane.RequestOutput, default_codec: Union[Type[ForwardRef('InputCodec')], ForwardRef('InputCodec'), NoneType] = None) -> mlserver.types.dataplane.ResponseOutput`


**Description:**
Helper to encode a high-level Python object into its corresponding
**response output**.
This method will find the most appropiate :doc:`input codec
</user-guide/content-type>` based on the model's metadata, request
output's content type or payload's type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### Method `encode_response`


**Signature:** `encode_response(self, payload: Any, default_codec: Union[Type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec'), NoneType] = None) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
Helper to encode a high-level Python object into its corresponding
**inference response**.
This method will find the most appropiate :doc:`request codec
</user-guide/content-type>` based on the payload's type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### Method `load`


**Signature:** `load(self) -> bool`


**Description:**
Method responsible for loading the model from a model artefact.
This method will be called on each of the parallel workers (when

### Method `metadata`


**Signature:** `metadata(self) -> mlserver.types.dataplane.MetadataModelResponse`


**Description:**
*No docstring available.*

### Method `predict`


**Signature:** `predict(self, payload: mlserver.types.dataplane.InferenceRequest) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
Method responsible for running inference on the model.
**This method can be overriden to implement your custom inference
logic.**

### Method `predict_stream`


**Signature:** `predict_stream(self, payloads: AsyncIterator[mlserver.types.dataplane.InferenceRequest]) -> AsyncIterator[mlserver.types.dataplane.InferenceResponse]`


**Description:**
Method responsible for running generation on the model, streaming a set
of responses back to the client.


**This method can be overriden to implement your custom inference
logic.**

### Method `unload`


**Signature:** `unload(self) -> bool`


**Description:**
Method responsible for unloading the model, freeing any resources (e.g.
CPU memory, GPU memory, etc.).
This method will be called on each of the parallel workers (when
