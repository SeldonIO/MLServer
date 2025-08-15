# Codecs — Built-ins

### *class* mlserver.codecs.NumpyCodec

Bases: [`InputCodec`](codecs-interfaces.md#mlserver.codecs.InputCodec)

Decodes an request input (response output) as a NumPy array.

#### ContentType *: ClassVar[str]* *= 'np'*

#### TypeHint

alias of `ndarray`

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*) – 
* **Return type:**
  bool

#### *classmethod* encode_output(name, payload, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*ndarray*) – 
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput)) – 
* **Return type:**
  *ndarray*

#### *classmethod* encode_input(name, payload, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*ndarray*) – 
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput)) – 
* **Return type:**
  *ndarray*

### *class* mlserver.codecs.NumpyRequestCodec

Bases: `SingleInputRequestCodec`

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

#### InputCodec

alias of [`NumpyCodec`](#mlserver.codecs.NumpyCodec)

#### ContentType *: ClassVar[str]* *= 'np'*

### *class* mlserver.codecs.StringCodec

Bases: [`InputCodec`](codecs-interfaces.md#mlserver.codecs.InputCodec)

Encodes a list of Python strings as a BYTES input (output).

#### ContentType *: ClassVar[str]* *= 'str'*

#### TypeHint

alias of `List`[`str`]

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*) – 
* **Return type:**
  bool

#### *classmethod* encode_output(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*List* *[**str* *]*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput)) – 
* **Return type:**
  *List*[str]

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput)) – 
* **Return type:**
  *List*[str]

#### *classmethod* encode_input(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*List* *[**str* *]*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

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

### *class* mlserver.codecs.Base64Codec

Bases: [`InputCodec`](codecs-interfaces.md#mlserver.codecs.InputCodec)

Codec that convers to / from a base64 input.

#### ContentType *: ClassVar[str]* *= 'base64'*

#### TypeHint

alias of `List`[`bytes`]

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*) – 
* **Return type:**
  bool

#### *classmethod* encode_output(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*List* *[**bytes* *]*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput)) – 
* **Return type:**
  *List*[bytes]

#### *classmethod* encode_input(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*List* *[**bytes* *]*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput)) – 
* **Return type:**
  *List*[bytes]

### *class* mlserver.codecs.DatetimeCodec

Bases: [`InputCodec`](codecs-interfaces.md#mlserver.codecs.InputCodec)

Codec that convers to / from a datetime input.

#### ContentType *: ClassVar[str]* *= 'datetime'*

#### TypeHint

alias of `List`[`Union`[`str`, `datetime`]]

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*) – 
* **Return type:**
  bool

#### *classmethod* encode_output(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*List* *[**str* *|* *datetime* *]*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput)) – 
* **Return type:**
  *List*[*datetime*]

#### *classmethod* encode_input(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*) – 
  * **payload** (*List* *[**str* *|* *datetime* *]*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput)) – 
* **Return type:**
  *List*[*datetime*]

### *class* mlserver.codecs.PandasCodec

Bases: [`RequestCodec`](codecs-interfaces.md#mlserver.codecs.RequestCodec)

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

#### ContentType *: ClassVar[str]* *= 'pd'*

#### JsonContentType *= 'pd_json'*

#### TypeHint

alias of `DataFrame`

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*) – 
* **Return type:**
  bool

#### *classmethod* encode_response(model_name, payload, model_version=None, use_bytes=True, \*\*kwargs)

Encode the given payload into an inference response.

* **Parameters:**
  * **model_name** (*str*) – 
  * **payload** (*DataFrame*) – 
  * **model_version** (*str* *|* *None*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*InferenceResponse*](types.md#mlserver.types.InferenceResponse)

#### *classmethod* decode_response(response)

Decode an inference response into a high-level Python object.

* **Parameters:**
  **response** ([*InferenceResponse*](types.md#mlserver.types.InferenceResponse)) – 
* **Return type:**
  *DataFrame*

#### *classmethod* encode_outputs(payload, use_bytes=True)

* **Parameters:**
  * **payload** (*DataFrame*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  *List*[[*ResponseOutput*](types.md#mlserver.types.ResponseOutput)]

#### *classmethod* encode_request(payload, use_bytes=True, \*\*kwargs)

Encode the given payload into an inference request.

* **Parameters:**
  * **payload** (*DataFrame*) – 
  * **use_bytes** (*bool*) – 
* **Return type:**
  [*InferenceRequest*](types.md#mlserver.types.InferenceRequest)

#### *classmethod* decode_request(request)

Decode an inference request into a high-level Python object.

* **Parameters:**
  **request** ([*InferenceRequest*](types.md#mlserver.types.InferenceRequest)) – 
* **Return type:**
  *DataFrame*
