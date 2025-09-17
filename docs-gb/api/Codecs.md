# Codecs

## Base64Codec

Codec that convers to / from a base64 input.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_input()

```python
decode_input(request_input: RequestInput) -> List[bytes]
```

Decode a request input into a high-level Python type.

### decode_output()

```python
decode_output(response_output: ResponseOutput) -> List[bytes]
```

Decode a response output into a high-level Python type.

### encode_input()

```python
encode_input(name: str, payload: List[bytes], use_bytes: bool = True, kwargs) -> RequestInput
```

Encode the given payload into a ``RequestInput``.

### encode_output()

```python
encode_output(name: str, payload: List[bytes], use_bytes: bool = True, kwargs) -> ResponseOutput
```

Encode the given payload into a response output.

## CodecError

### Methods

### add_note()

```python
add_note(...)
```

Exception.add_note(note) --
add a note to the exception

### with_traceback()

```python
with_traceback(...)
```

Exception.with_traceback(tb) --
set self.__traceback__ to tb and return self.

## DatetimeCodec

Codec that convers to / from a datetime input.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_input()

```python
decode_input(request_input: RequestInput) -> List[datetime]
```

Decode a request input into a high-level Python type.

### decode_output()

```python
decode_output(response_output: ResponseOutput) -> List[datetime]
```

Decode a response output into a high-level Python type.

### encode_input()

```python
encode_input(name: str, payload: List[Union[str, datetime]], use_bytes: bool = True, kwargs) -> RequestInput
```

Encode the given payload into a ``RequestInput``.

### encode_output()

```python
encode_output(name: str, payload: List[Union[str, datetime]], use_bytes: bool = True, kwargs) -> ResponseOutput
```

Encode the given payload into a response output.

## InputCodec

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
``RequestCodec`` interface instead.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_input()

```python
decode_input(request_input: RequestInput) -> Any
```

Decode a request input into a high-level Python type.

### decode_output()

```python
decode_output(response_output: ResponseOutput) -> Any
```

Decode a response output into a high-level Python type.

### encode_input()

```python
encode_input(name: str, payload: Any, kwargs) -> RequestInput
```

Encode the given payload into a ``RequestInput``.

### encode_output()

```python
encode_output(name: str, payload: Any, kwargs) -> ResponseOutput
```

Encode the given payload into a response output.

## NumpyCodec

Decodes an request input (response output) as a NumPy array.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_input()

```python
decode_input(request_input: RequestInput) -> ndarray
```

Decode a request input into a high-level Python type.

### decode_output()

```python
decode_output(response_output: ResponseOutput) -> ndarray
```

Decode a response output into a high-level Python type.

### encode_input()

```python
encode_input(name: str, payload: ndarray, kwargs) -> RequestInput
```

Encode the given payload into a ``RequestInput``.

### encode_output()

```python
encode_output(name: str, payload: ndarray, kwargs) -> ResponseOutput
```

Encode the given payload into a response output.

## NumpyRequestCodec

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_request()

```python
decode_request(request: InferenceRequest) -> Any
```

Decode an inference request into a high-level Python object.

### decode_response()

```python
decode_response(response: InferenceResponse) -> Any
```

Decode an inference response into a high-level Python object.

### encode_request()

```python
encode_request(payload: Any, kwargs) -> InferenceRequest
```

Encode the given payload into an inference request.

### encode_response()

```python
encode_response(model_name: str, payload: Any, model_version: Optional[str] = None, kwargs) -> InferenceResponse
```

Encode the given payload into an inference response.

## PandasCodec

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_request()

```python
decode_request(request: InferenceRequest) -> DataFrame
```

Decode an inference request into a high-level Python object.

### decode_response()

```python
decode_response(response: InferenceResponse) -> DataFrame
```

Decode an inference response into a high-level Python object.

### encode_outputs()

```python
encode_outputs(payload: DataFrame, use_bytes: bool = True) -> List[ResponseOutput]
```

### encode_request()

```python
encode_request(payload: DataFrame, use_bytes: bool = True, kwargs) -> InferenceRequest
```

Encode the given payload into an inference request.

### encode_response()

```python
encode_response(model_name: str, payload: DataFrame, model_version: Optional[str] = None, use_bytes: bool = True, kwargs) -> InferenceResponse
```

Encode the given payload into an inference response.

## RequestCodec

The ``RequestCodec`` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the ``InputCodec``
interface instead.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_request()

```python
decode_request(request: InferenceRequest) -> Any
```

Decode an inference request into a high-level Python object.

### decode_response()

```python
decode_response(response: InferenceResponse) -> Any
```

Decode an inference response into a high-level Python object.

### encode_request()

```python
encode_request(payload: Any, kwargs) -> InferenceRequest
```

Encode the given payload into an inference request.

### encode_response()

```python
encode_response(model_name: str, payload: Any, model_version: Optional[str] = None, kwargs) -> InferenceResponse
```

Encode the given payload into an inference response.

## StringCodec

Encodes a list of Python strings as a BYTES input (output).

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_input()

```python
decode_input(request_input: RequestInput) -> List[str]
```

Decode a request input into a high-level Python type.

### decode_output()

```python
decode_output(response_output: ResponseOutput) -> List[str]
```

Decode a response output into a high-level Python type.

### encode_input()

```python
encode_input(name: str, payload: List[str], use_bytes: bool = True, kwargs) -> RequestInput
```

Encode the given payload into a ``RequestInput``.

### encode_output()

```python
encode_output(name: str, payload: List[str], use_bytes: bool = True, kwargs) -> ResponseOutput
```

Encode the given payload into a response output.

## StringRequestCodec

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

### Methods

### can_encode()

```python
can_encode(payload: Any) -> bool
```

Evaluate whether the codec can encode (decode) the payload.

### decode_request()

```python
decode_request(request: InferenceRequest) -> Any
```

Decode an inference request into a high-level Python object.

### decode_response()

```python
decode_response(response: InferenceResponse) -> Any
```

Decode an inference response into a high-level Python object.

### encode_request()

```python
encode_request(payload: Any, kwargs) -> InferenceRequest
```

Encode the given payload into an inference request.

### encode_response()

```python
encode_response(model_name: str, payload: Any, model_version: Optional[str] = None, kwargs) -> InferenceResponse
```

Encode the given payload into an inference response.

## decode_args()

```python
decode_args(predict: Callable) -> Callable[[ForwardRef('MLModel'), <class 'mlserver.types.dataplane.InferenceRequest'>], Coroutine[Any, Any, InferenceResponse]]
```

_No description available._

## decode_inference_request()

```python
decode_inference_request(inference_request: InferenceRequest, model_settings: Optional[ModelSettings] = None, metadata_inputs: Dict[str, MetadataTensor] = {}) -> Optional[Any]
```

_No description available._

## decode_request_input()

```python
decode_request_input(request_input: RequestInput, metadata_inputs: Dict[str, MetadataTensor] = {}) -> Optional[Any]
```

_No description available._

## encode_inference_response()

```python
encode_inference_response(payload: Any, model_settings: ModelSettings) -> Optional[InferenceResponse]
```

_No description available._

## encode_response_output()

```python
encode_response_output(payload: Any, request_output: RequestOutput, metadata_outputs: Dict[str, MetadataTensor] = {}) -> Optional[ResponseOutput]
```

_No description available._

## get_decoded()

```python
get_decoded(parametrised_obj: Union[InferenceRequest, RequestInput, RequestOutput, ResponseOutput, InferenceResponse]) -> Any
```

_No description available._

## get_decoded_or_raw()

```python
get_decoded_or_raw(parametrised_obj: Union[InferenceRequest, RequestInput, RequestOutput, ResponseOutput, InferenceResponse]) -> Any
```

_No description available._

## has_decoded()

```python
has_decoded(parametrised_obj: Union[InferenceRequest, RequestInput, RequestOutput, ResponseOutput, InferenceResponse]) -> bool
```

_No description available._

## register_input_codec()

```python
register_input_codec(CodecKlass: Union[type[InputCodec], InputCodec])
```

_No description available._

## register_request_codec()

```python
register_request_codec(CodecKlass: Union[type[RequestCodec], RequestCodec])
```

_No description available._

