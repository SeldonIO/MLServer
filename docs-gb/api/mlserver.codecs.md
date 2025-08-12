# mlserver.codecs

### *exception* mlserver.codecs.CodecError(msg: str)

Bases: `MLServerError`

#### add_note()

Exception.add_note(note) –
add a note to the exception

#### args

#### with_traceback()

Exception.with_traceback(tb) –
set self._\_traceback_\_ to tb and return self.

### *class* mlserver.codecs.NumpyCodec

Bases: [`InputCodec`](#mlserver.codecs.InputCodec)

Decodes an request input (response output) as a NumPy array.

#### ContentType *: ClassVar[str]* *= 'np'*

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_output(name: str, payload: numpy.ndarray, \*\*kwargs)

Encode the given payload into a response output.

#### *classmethod* decode_output(response_output: [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput))

Decode a response output into a high-level Python type.

#### *classmethod* encode_input(name: str, payload: numpy.ndarray, \*\*kwargs)

Encode the given payload into a `RequestInput`.

#### *classmethod* decode_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

Decode a request input into a high-level Python type.

#### *classmethod* decode(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

#### *classmethod* encode(name: str, payload: Any)

### *class* mlserver.codecs.NumpyRequestCodec

Bases: `SingleInputRequestCodec`

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

#### InputCodec

alias of [`NumpyCodec`](#mlserver.codecs.NumpyCodec)

#### ContentType *: ClassVar[str]* *= 'np'*

#### TypeHint

alias of `None`

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* decode(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

#### *classmethod* decode_request(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Decode an inference request into a high-level Python object.

#### *classmethod* decode_response(response: [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

Decode an inference response into a high-level Python object.

#### *classmethod* encode(model_name: str, payload: Any, model_version: str | None = None)

#### *classmethod* encode_request(payload: Any, \*\*kwargs)

Encode the given payload into an inference request.

#### *classmethod* encode_response(model_name: str, payload: Any, model_version: str | None = None, \*\*kwargs)

Encode the given payload into an inference response.

### *class* mlserver.codecs.StringCodec

Bases: [`InputCodec`](#mlserver.codecs.InputCodec)

Encodes a list of Python strings as a BYTES input (output).

#### ContentType *: ClassVar[str]* *= 'str'*

#### TypeHint

alias of `List`[`str`]

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_output(name: str, payload: List[str], use_bytes: bool = True, \*\*kwargs)

Encode the given payload into a response output.

#### *classmethod* decode_output(response_output: [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput))

Decode a response output into a high-level Python type.

#### *classmethod* decode_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

Decode a request input into a high-level Python type.

#### *classmethod* encode_input(name: str, payload: List[str], use_bytes: bool = True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

#### *classmethod* decode(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

#### *classmethod* encode(name: str, payload: Any)

### *class* mlserver.codecs.StringRequestCodec

Bases: `SingleInputRequestCodec`

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

#### InputCodec

alias of [`StringCodec`](#mlserver.codecs.StringCodec)

#### ContentType *: ClassVar[str]* *= 'str'*

#### TypeHint

alias of `List`[`str`]

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* decode(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

#### *classmethod* decode_request(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Decode an inference request into a high-level Python object.

#### *classmethod* decode_response(response: [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

Decode an inference response into a high-level Python object.

#### *classmethod* encode(model_name: str, payload: Any, model_version: str | None = None)

#### *classmethod* encode_request(payload: Any, \*\*kwargs)

Encode the given payload into an inference request.

#### *classmethod* encode_response(model_name: str, payload: Any, model_version: str | None = None, \*\*kwargs)

Encode the given payload into an inference response.

### *class* mlserver.codecs.Base64Codec

Bases: [`InputCodec`](#mlserver.codecs.InputCodec)

Codec that convers to / from a base64 input.

#### ContentType *: ClassVar[str]* *= 'base64'*

#### TypeHint

alias of `List`[`bytes`]

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_output(name: str, payload: List[bytes], use_bytes: bool = True, \*\*kwargs)

Encode the given payload into a response output.

#### *classmethod* decode_output(response_output: [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput))

Decode a response output into a high-level Python type.

#### *classmethod* encode_input(name: str, payload: List[bytes], use_bytes: bool = True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

#### *classmethod* decode_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

Decode a request input into a high-level Python type.

#### *classmethod* decode(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

#### *classmethod* encode(name: str, payload: Any)

### *class* mlserver.codecs.DatetimeCodec

Bases: [`InputCodec`](#mlserver.codecs.InputCodec)

Codec that convers to / from a datetime input.

#### ContentType *: ClassVar[str]* *= 'datetime'*

#### TypeHint

alias of `List`[`Union`[`str`, `datetime`]]

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_output(name: str, payload: List[str | datetime], use_bytes: bool = True, \*\*kwargs)

Encode the given payload into a response output.

#### *classmethod* decode_output(response_output: [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput))

Decode a response output into a high-level Python type.

#### *classmethod* encode_input(name: str, payload: List[str | datetime], use_bytes: bool = True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

#### *classmethod* decode_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

Decode a request input into a high-level Python type.

#### *classmethod* decode(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

#### *classmethod* encode(name: str, payload: Any)

### *class* mlserver.codecs.PandasCodec

Bases: [`RequestCodec`](#mlserver.codecs.RequestCodec)

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

#### ContentType *: ClassVar[str]* *= 'pd'*

#### JsonContentType *= 'pd_json'*

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_response(model_name: str, payload: pandas.DataFrame, model_version: str | None = None, use_bytes: bool = True, \*\*kwargs)

Encode the given payload into an inference response.

#### *classmethod* decode_response(response: [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

Decode an inference response into a high-level Python object.

#### *classmethod* encode_outputs(payload: pandas.DataFrame, use_bytes: bool = True)

#### *classmethod* encode_request(payload: pandas.DataFrame, use_bytes: bool = True, \*\*kwargs)

Encode the given payload into an inference request.

#### *classmethod* decode_request(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Decode an inference request into a high-level Python object.

#### *classmethod* decode(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

#### *classmethod* encode(model_name: str, payload: Any, model_version: str | None = None)

### *class* mlserver.codecs.InputCodec

Bases: `object`

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
`RequestCodec` interface instead.

#### ContentType *: ClassVar[str]* *= ''*

#### TypeHint

alias of `None`

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode(name: str, payload: Any)

#### *classmethod* encode_output(name: str, payload: Any, \*\*kwargs)

Encode the given payload into a response output.

#### *classmethod* decode_output(response_output: [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput))

Decode a response output into a high-level Python type.

#### *classmethod* encode_input(name: str, payload: Any, \*\*kwargs)

Encode the given payload into a `RequestInput`.

#### *classmethod* decode(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

#### *classmethod* decode_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

Decode a request input into a high-level Python type.

### *class* mlserver.codecs.RequestCodec

Bases: `object`

The `RequestCodec` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the `InputCodec`
interface instead.

#### ContentType *: ClassVar[str]* *= ''*

#### TypeHint

alias of `None`

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode(model_name: str, payload: Any, model_version: str | None = None)

#### *classmethod* encode_response(model_name: str, payload: Any, model_version: str | None = None, \*\*kwargs)

Encode the given payload into an inference response.

#### *classmethod* decode_response(response: [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

Decode an inference response into a high-level Python object.

#### *classmethod* encode_request(payload: Any, \*\*kwargs)

Encode the given payload into an inference request.

#### *classmethod* decode(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

#### *classmethod* decode_request(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Decode an inference request into a high-level Python object.

### mlserver.codecs.register_input_codec(CodecKlass: Type[[InputCodec](#mlserver.codecs.InputCodec)] | [InputCodec](#mlserver.codecs.InputCodec))

### mlserver.codecs.register_request_codec(CodecKlass: Type[[RequestCodec](#mlserver.codecs.RequestCodec)] | [RequestCodec](#mlserver.codecs.RequestCodec))

### mlserver.codecs.has_decoded(parametrised_obj: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest) | [RequestInput](mlserver.types.md#mlserver.types.RequestInput) | [RequestOutput](mlserver.types.md#mlserver.types.RequestOutput) | [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput) | [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

### mlserver.codecs.get_decoded(parametrised_obj: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest) | [RequestInput](mlserver.types.md#mlserver.types.RequestInput) | [RequestOutput](mlserver.types.md#mlserver.types.RequestOutput) | [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput) | [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

### mlserver.codecs.get_decoded_or_raw(parametrised_obj: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest) | [RequestInput](mlserver.types.md#mlserver.types.RequestInput) | [RequestOutput](mlserver.types.md#mlserver.types.RequestOutput) | [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput) | [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

### mlserver.codecs.encode_inference_response(payload: Any, model_settings: ModelSettings)

### mlserver.codecs.encode_response_output(payload: Any, request_output: [RequestOutput](mlserver.types.md#mlserver.types.RequestOutput), metadata_outputs: Dict[str, [MetadataTensor](mlserver.types.md#mlserver.types.MetadataTensor)] = {})

### mlserver.codecs.decode_request_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput), metadata_inputs: Dict[str, [MetadataTensor](mlserver.types.md#mlserver.types.MetadataTensor)] = {})

### mlserver.codecs.decode_inference_request(inference_request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest), model_settings: ModelSettings | None = None, metadata_inputs: Dict[str, [MetadataTensor](mlserver.types.md#mlserver.types.MetadataTensor)] = {})

### mlserver.codecs.decode_args(predict: Callable)
