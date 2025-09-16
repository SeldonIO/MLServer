# Codecs

## Methods

# Module `mlserver.codecs`

## Class `Base64Codec`

Codec that convers to / from a base64 input.

### Methods

## Class `CodecError`

### Methods

## Class `DatetimeCodec`

Codec that convers to / from a datetime input.

### Methods

## Class `InputCodec`

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
``RequestCodec`` interface instead.

### Methods

## Class `NumpyCodec`

Decodes an request input (response output) as a NumPy array.

### Methods

## Class `NumpyRequestCodec`

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

### Methods

## Class `PandasCodec`

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

### Methods

## Class `RequestCodec`

The ``RequestCodec`` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the ``InputCodec``
interface instead.

### Methods

## Class `StringCodec`

Encodes a list of Python strings as a BYTES input (output).

### Methods

## Class `StringRequestCodec`

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

### Methods

## Function `decode_args`

```python
decode_args(predict: Callable) -> Callable[[ForwardRef('MLModel'), mlserver.types.dataplane.InferenceRequest], Coroutine[Any, Any, mlserver.types.dataplane.InferenceResponse]]
```

-

## Function `decode_inference_request`

```python
decode_inference_request(inference_request: mlserver.types.dataplane.InferenceRequest, model_settings: Optional[mlserver.settings.ModelSettings] = None, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```

-

## Function `decode_request_input`

```python
decode_request_input(request_input: mlserver.types.dataplane.RequestInput, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```

-

## Function `encode_inference_response`

```python
encode_inference_response(payload: Any, model_settings: mlserver.settings.ModelSettings) -> Optional[mlserver.types.dataplane.InferenceResponse]
```

-

## Function `encode_response_output`

```python
encode_response_output(payload: Any, request_output: mlserver.types.dataplane.RequestOutput, metadata_outputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[mlserver.types.dataplane.ResponseOutput]
```

-

## Function `get_decoded`

```python
get_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```

-

## Function `get_decoded_or_raw`

```python
get_decoded_or_raw(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```

-

## Function `has_decoded`

```python
has_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> bool
```

-

## Function `register_input_codec`

```python
register_input_codec(CodecKlass: Union[Type[ForwardRef('InputCodec')], ForwardRef('InputCodec')])
```

-

## Function `register_request_codec`

```python
register_request_codec(CodecKlass: Union[Type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec')])
```

-


