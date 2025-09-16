# Codecs

## Methods

# Module `mlserver.codecs`

## Class `Base64Codec`

Codec that convers to / from a base64 input.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request_input: mlserver.types.dataplane.RequestInput) -> Any
```
-

### `decode_input`
```python
decode_input(request_input: mlserver.types.dataplane.RequestInput) -> List[bytes]
```
Decode a request input into a high-level Python type.

### `decode_output`
```python
decode_output(response_output: mlserver.types.dataplane.ResponseOutput) -> List[bytes]
```
Decode a response output into a high-level Python type.

### `encode`
```python
encode(name: str, payload: Any) -> mlserver.types.dataplane.ResponseOutput
```
-

### `encode_input`
```python
encode_input(name: str, payload: List[bytes], use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.RequestInput
```
Encode the given payload into a ``RequestInput``.

### `encode_output`
```python
encode_output(name: str, payload: List[bytes], use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.ResponseOutput
```
Encode the given payload into a response output.

## Class `CodecError`

### Methods

## Class `DatetimeCodec`

Codec that convers to / from a datetime input.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request_input: mlserver.types.dataplane.RequestInput) -> Any
```
-

### `decode_input`
```python
decode_input(request_input: mlserver.types.dataplane.RequestInput) -> List[datetime.datetime]
```
Decode a request input into a high-level Python type.

### `decode_output`
```python
decode_output(response_output: mlserver.types.dataplane.ResponseOutput) -> List[datetime.datetime]
```
Decode a response output into a high-level Python type.

### `encode`
```python
encode(name: str, payload: Any) -> mlserver.types.dataplane.ResponseOutput
```
-

### `encode_input`
```python
encode_input(name: str, payload: List[Union[str, datetime.datetime]], use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.RequestInput
```
Encode the given payload into a ``RequestInput``.

### `encode_output`
```python
encode_output(name: str, payload: List[Union[str, datetime.datetime]], use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.ResponseOutput
```
Encode the given payload into a response output.

## Class `InputCodec`

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
``RequestCodec`` interface instead.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request_input: mlserver.types.dataplane.RequestInput) -> Any
```
-

### `decode_input`
```python
decode_input(request_input: mlserver.types.dataplane.RequestInput) -> Any
```
Decode a request input into a high-level Python type.

### `decode_output`
```python
decode_output(response_output: mlserver.types.dataplane.ResponseOutput) -> Any
```
Decode a response output into a high-level Python type.

### `encode`
```python
encode(name: str, payload: Any) -> mlserver.types.dataplane.ResponseOutput
```
-

### `encode_input`
```python
encode_input(name: str, payload: Any, **kwargs) -> mlserver.types.dataplane.RequestInput
```
Encode the given payload into a ``RequestInput``.

### `encode_output`
```python
encode_output(name: str, payload: Any, **kwargs) -> mlserver.types.dataplane.ResponseOutput
```
Encode the given payload into a response output.

## Class `NumpyCodec`

Decodes an request input (response output) as a NumPy array.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request_input: mlserver.types.dataplane.RequestInput) -> Any
```
-

### `decode_input`
```python
decode_input(request_input: mlserver.types.dataplane.RequestInput) -> numpy.ndarray
```
Decode a request input into a high-level Python type.

### `decode_output`
```python
decode_output(response_output: mlserver.types.dataplane.ResponseOutput) -> numpy.ndarray
```
Decode a response output into a high-level Python type.

### `encode`
```python
encode(name: str, payload: Any) -> mlserver.types.dataplane.ResponseOutput
```
-

### `encode_input`
```python
encode_input(name: str, payload: numpy.ndarray, **kwargs) -> mlserver.types.dataplane.RequestInput
```
Encode the given payload into a ``RequestInput``.

### `encode_output`
```python
encode_output(name: str, payload: numpy.ndarray, **kwargs) -> mlserver.types.dataplane.ResponseOutput
```
Encode the given payload into a response output.

## Class `NumpyRequestCodec`

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
-

### `decode_request`
```python
decode_request(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
Decode an inference request into a high-level Python object.

### `decode_response`
```python
decode_response(response: mlserver.types.dataplane.InferenceResponse) -> Any
```
Decode an inference response into a high-level Python object.

### `encode`
```python
encode(model_name: str, payload: Any, model_version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse
```
-

### `encode_request`
```python
encode_request(payload: Any, **kwargs) -> mlserver.types.dataplane.InferenceRequest
```
Encode the given payload into an inference request.

### `encode_response`
```python
encode_response(model_name: str, payload: Any, model_version: Optional[str] = None, **kwargs) -> mlserver.types.dataplane.InferenceResponse
```
Encode the given payload into an inference response.

## Class `PandasCodec`

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
-

### `decode_request`
```python
decode_request(request: mlserver.types.dataplane.InferenceRequest) -> pandas.core.frame.DataFrame
```
Decode an inference request into a high-level Python object.

### `decode_response`
```python
decode_response(response: mlserver.types.dataplane.InferenceResponse) -> pandas.core.frame.DataFrame
```
Decode an inference response into a high-level Python object.

### `encode`
```python
encode(model_name: str, payload: Any, model_version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse
```
-

### `encode_outputs`
```python
encode_outputs(payload: pandas.core.frame.DataFrame, use_bytes: bool = True) -> List[mlserver.types.dataplane.ResponseOutput]
```
-

### `encode_request`
```python
encode_request(payload: pandas.core.frame.DataFrame, use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.InferenceRequest
```
Encode the given payload into an inference request.

### `encode_response`
```python
encode_response(model_name: str, payload: pandas.core.frame.DataFrame, model_version: Optional[str] = None, use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.InferenceResponse
```
Encode the given payload into an inference response.

## Class `RequestCodec`

The ``RequestCodec`` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the ``InputCodec``
interface instead.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
-

### `decode_request`
```python
decode_request(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
Decode an inference request into a high-level Python object.

### `decode_response`
```python
decode_response(response: mlserver.types.dataplane.InferenceResponse) -> Any
```
Decode an inference response into a high-level Python object.

### `encode`
```python
encode(model_name: str, payload: Any, model_version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse
```
-

### `encode_request`
```python
encode_request(payload: Any, **kwargs) -> mlserver.types.dataplane.InferenceRequest
```
Encode the given payload into an inference request.

### `encode_response`
```python
encode_response(model_name: str, payload: Any, model_version: Optional[str] = None, **kwargs) -> mlserver.types.dataplane.InferenceResponse
```
Encode the given payload into an inference response.

## Class `StringCodec`

Encodes a list of Python strings as a BYTES input (output).

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request_input: mlserver.types.dataplane.RequestInput) -> Any
```
-

### `decode_input`
```python
decode_input(request_input: mlserver.types.dataplane.RequestInput) -> List[str]
```
Decode a request input into a high-level Python type.

### `decode_output`
```python
decode_output(response_output: mlserver.types.dataplane.ResponseOutput) -> List[str]
```
Decode a response output into a high-level Python type.

### `encode`
```python
encode(name: str, payload: Any) -> mlserver.types.dataplane.ResponseOutput
```
-

### `encode_input`
```python
encode_input(name: str, payload: List[str], use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.RequestInput
```
Encode the given payload into a ``RequestInput``.

### `encode_output`
```python
encode_output(name: str, payload: List[str], use_bytes: bool = True, **kwargs) -> mlserver.types.dataplane.ResponseOutput
```
Encode the given payload into a response output.

## Class `StringRequestCodec`

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

### Methods

### `can_encode`
```python
can_encode(payload: Any) -> bool
```
Evaluate whether the codec can encode (decode) the payload.

### `decode`
```python
decode(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
-

### `decode_request`
```python
decode_request(request: mlserver.types.dataplane.InferenceRequest) -> Any
```
Decode an inference request into a high-level Python object.

### `decode_response`
```python
decode_response(response: mlserver.types.dataplane.InferenceResponse) -> Any
```
Decode an inference response into a high-level Python object.

### `encode`
```python
encode(model_name: str, payload: Any, model_version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse
```
-

### `encode_request`
```python
encode_request(payload: Any, **kwargs) -> mlserver.types.dataplane.InferenceRequest
```
Encode the given payload into an inference request.

### `encode_response`
```python
encode_response(model_name: str, payload: Any, model_version: Optional[str] = None, **kwargs) -> mlserver.types.dataplane.InferenceResponse
```
Encode the given payload into an inference response.

## Function `decode_args`

### `decode_args`
```python
decode_args(predict: Callable) -> Callable[[ForwardRef('MLModel'), mlserver.types.dataplane.InferenceRequest], Coroutine[Any, Any, mlserver.types.dataplane.InferenceResponse]]
```
-

## Function `decode_inference_request`

### `decode_inference_request`
```python
decode_inference_request(inference_request: mlserver.types.dataplane.InferenceRequest, model_settings: Optional[mlserver.settings.ModelSettings] = None, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```
-

## Function `decode_request_input`

### `decode_request_input`
```python
decode_request_input(request_input: mlserver.types.dataplane.RequestInput, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```
-

## Function `encode_inference_response`

### `encode_inference_response`
```python
encode_inference_response(payload: Any, model_settings: mlserver.settings.ModelSettings) -> Optional[mlserver.types.dataplane.InferenceResponse]
```
-

## Function `encode_response_output`

### `encode_response_output`
```python
encode_response_output(payload: Any, request_output: mlserver.types.dataplane.RequestOutput, metadata_outputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[mlserver.types.dataplane.ResponseOutput]
```
-

## Function `get_decoded`

### `get_decoded`
```python
get_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```
-

## Function `get_decoded_or_raw`

### `get_decoded_or_raw`
```python
get_decoded_or_raw(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```
-

## Function `has_decoded`

### `has_decoded`
```python
has_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> bool
```
-

## Function `register_input_codec`

### `register_input_codec`
```python
register_input_codec(CodecKlass: Union[Type[ForwardRef('InputCodec')], ForwardRef('InputCodec')])
```
-

## Function `register_request_codec`

### `register_request_codec`
```python
register_request_codec(CodecKlass: Union[Type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec')])
```
-


