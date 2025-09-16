# Codecs

## Base64Codec

Codec that convers to / from a base64 input.

## CodecError

Common base class for all non-exit exceptions.

## DatetimeCodec

Codec that convers to / from a datetime input.

## InputCodec

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
``RequestCodec`` interface instead.

## NumpyCodec

Decodes an request input (response output) as a NumPy array.

## NumpyRequestCodec

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

## PandasCodec

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

## RequestCodec

The ``RequestCodec`` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the ``InputCodec``
interface instead.

## StringCodec

Encodes a list of Python strings as a BYTES input (output).

## StringRequestCodec

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

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

