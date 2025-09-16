# MLModel

Abstract inference runtime which exposes the main interface to interact
with ML models.

## Methods

### decode()

```python
decode(request_input: RequestInput, default_codec: Union[type[ForwardRef('InputCodec')], ForwardRef('InputCodec'), None] = None) -> Any
```

Helper to decode a **request input** into its corresponding high-level
Python object.
This method will find the most appropiate :doc:`input codec
</user-guide/content-type>` based on the model's metadata and the
input's content type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### decode_request()

```python
decode_request(inference_request: InferenceRequest, default_codec: Union[type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec'), None] = None) -> Any
```

Helper to decode an **inference request** into its corresponding
high-level Python object.
This method will find the most appropiate :doc:`request codec
</user-guide/content-type>` based on the model's metadata and the
requests's content type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### encode()

```python
encode(payload: Any, request_output: RequestOutput, default_codec: Union[type[ForwardRef('InputCodec')], ForwardRef('InputCodec'), None] = None) -> ResponseOutput
```

Helper to encode a high-level Python object into its corresponding
**response output**.
This method will find the most appropiate :doc:`input codec
</user-guide/content-type>` based on the model's metadata, request
output's content type or payload's type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### encode_response()

```python
encode_response(payload: Any, default_codec: Union[type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec'), None] = None) -> InferenceResponse
```

Helper to encode a high-level Python object into its corresponding
**inference response**.
This method will find the most appropiate :doc:`request codec
</user-guide/content-type>` based on the payload's type.
Otherwise, it will fall back to the codec specified in the
``default_codec`` kwarg.

### load()

```python
load() -> bool
```

Method responsible for loading the model from a model artefact.
This method will be called on each of the parallel workers (when
:doc:`parallel inference </user-guide/parallel-inference>`) is
enabled).
Its return value will represent the model's readiness status.
A return value of ``True`` will mean the model is ready.

**This method can be overriden to implement your custom load
logic.**

### metadata()

```python
metadata() -> MetadataModelResponse
```

_No description available._

### predict()

```python
predict(payload: InferenceRequest) -> InferenceResponse
```

Method responsible for running inference on the model.


**This method can be overriden to implement your custom inference
logic.**

### predict_stream()

```python
predict_stream(payloads: AsyncIterator[InferenceRequest]) -> AsyncIterator[InferenceResponse]
```

Method responsible for running generation on the model, streaming a set
of responses back to the client.


**This method can be overriden to implement your custom inference
logic.**

### unload()

```python
unload() -> bool
```

Method responsible for unloading the model, freeing any resources (e.g.
CPU memory, GPU memory, etc.).
This method will be called on each of the parallel workers (when
:doc:`parallel inference </user-guide/parallel-inference>`) is
enabled).
A return value of ``True`` will mean the model is now unloaded.

**This method can be overriden to implement your custom unload
logic.**

