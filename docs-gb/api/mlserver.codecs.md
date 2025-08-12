# mlserver.codecs

### *exception* CodecError(msg: str)

### *class* NumpyCodec

Decodes an request input (response output) as a NumPy array.

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

### *class* NumpyRequestCodec

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

#### InputCodec

alias of [`NumpyCodec`](#mlserver.codecs.NumpyCodec)

### *class* StringCodec

Encodes a list of Python strings as a BYTES input (output).

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

### *class* StringRequestCodec

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

#### InputCodec

alias of [`StringCodec`](#mlserver.codecs.StringCodec)

### *class* Base64Codec

Codec that convers to / from a base64 input.

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

### *class* DatetimeCodec

Codec that convers to / from a datetime input.

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

### *class* PandasCodec

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_response(model_name: str, payload: pandas.DataFrame, model_version: str | None = None, use_bytes: bool = True, \*\*kwargs)

Encode the given payload into an inference response.

#### *classmethod* decode_response(response: [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

Decode an inference response into a high-level Python object.

#### *classmethod* encode_request(payload: pandas.DataFrame, use_bytes: bool = True, \*\*kwargs)

Encode the given payload into an inference request.

#### *classmethod* decode_request(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Decode an inference request into a high-level Python object.

### *class* InputCodec

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
`RequestCodec` interface instead.

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_output(name: str, payload: Any, \*\*kwargs)

Encode the given payload into a response output.

#### *classmethod* decode_output(response_output: [ResponseOutput](mlserver.types.md#mlserver.types.ResponseOutput))

Decode a response output into a high-level Python type.

#### *classmethod* encode_input(name: str, payload: Any, \*\*kwargs)

Encode the given payload into a `RequestInput`.

#### *classmethod* decode_input(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput))

Decode a request input into a high-level Python type.

### *class* RequestCodec

The `RequestCodec` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the `InputCodec`
interface instead.

#### *classmethod* can_encode(payload: Any)

Evaluate whether the codec can encode (decode) the payload.

#### *classmethod* encode_response(model_name: str, payload: Any, model_version: str | None = None, \*\*kwargs)

Encode the given payload into an inference response.

#### *classmethod* decode_response(response: [InferenceResponse](mlserver.types.md#mlserver.types.InferenceResponse))

Decode an inference response into a high-level Python object.

#### *classmethod* encode_request(payload: Any, \*\*kwargs)

Encode the given payload into an inference request.

#### *classmethod* decode_request(request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Decode an inference request into a high-level Python object.
