<a id="codecs-built-ins"></a>

# Codecs — Built-ins

<a id="mlserver.codecs.NumpyCodec"></a>

### *class* mlserver.codecs.NumpyCodec

Decodes an request input (response output) as a NumPy array.

<a id="mlserver.codecs.NumpyCodec.TypeHint"></a>

#### TypeHint

alias of `ndarray`

<a id="mlserver.codecs.NumpyCodec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.NumpyCodec.encode_output"></a>

#### *classmethod* encode_output(name, payload, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*ndarray*)
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

<a id="mlserver.codecs.NumpyCodec.decode_output"></a>

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))
* **Return type:**
  *ndarray*

<a id="mlserver.codecs.NumpyCodec.encode_input"></a>

#### *classmethod* encode_input(name, payload, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*ndarray*)
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

<a id="mlserver.codecs.NumpyCodec.decode_input"></a>

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))
* **Return type:**
  *ndarray*

<a id="mlserver.codecs.NumpyRequestCodec"></a>

### *class* mlserver.codecs.NumpyRequestCodec

Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

<a id="mlserver.codecs.NumpyRequestCodec.InputCodec"></a>

#### InputCodec

alias of [`NumpyCodec`](#mlserver.codecs.NumpyCodec)

<a id="mlserver.codecs.StringCodec"></a>

### *class* mlserver.codecs.StringCodec

Encodes a list of Python strings as a BYTES input (output).

<a id="mlserver.codecs.StringCodec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.StringCodec.encode_output"></a>

#### *classmethod* encode_output(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*List* *[**str* *]*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

<a id="mlserver.codecs.StringCodec.decode_output"></a>

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))
* **Return type:**
  *List*[str]

<a id="mlserver.codecs.StringCodec.decode_input"></a>

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))
* **Return type:**
  *List*[str]

<a id="mlserver.codecs.StringCodec.encode_input"></a>

#### *classmethod* encode_input(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*List* *[**str* *]*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

<a id="mlserver.codecs.StringRequestCodec"></a>

### *class* mlserver.codecs.StringRequestCodec

Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

<a id="mlserver.codecs.StringRequestCodec.InputCodec"></a>

#### InputCodec

alias of [`StringCodec`](#mlserver.codecs.StringCodec)

<a id="mlserver.codecs.Base64Codec"></a>

### *class* mlserver.codecs.Base64Codec

Codec that convers to / from a base64 input.

<a id="mlserver.codecs.Base64Codec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.Base64Codec.encode_output"></a>

#### *classmethod* encode_output(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*List* *[**bytes* *]*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

<a id="mlserver.codecs.Base64Codec.decode_output"></a>

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))
* **Return type:**
  *List*[bytes]

<a id="mlserver.codecs.Base64Codec.encode_input"></a>

#### *classmethod* encode_input(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*List* *[**bytes* *]*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

<a id="mlserver.codecs.Base64Codec.decode_input"></a>

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))
* **Return type:**
  *List*[bytes]

<a id="mlserver.codecs.DatetimeCodec"></a>

### *class* mlserver.codecs.DatetimeCodec

Codec that convers to / from a datetime input.

<a id="mlserver.codecs.DatetimeCodec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.DatetimeCodec.encode_output"></a>

#### *classmethod* encode_output(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*List* *[**str* *|* *datetime* *]*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

<a id="mlserver.codecs.DatetimeCodec.decode_output"></a>

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))
* **Return type:**
  *List*[*datetime*]

<a id="mlserver.codecs.DatetimeCodec.encode_input"></a>

#### *classmethod* encode_input(name, payload, use_bytes=True, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*List* *[**str* *|* *datetime* *]*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

<a id="mlserver.codecs.DatetimeCodec.decode_input"></a>

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))
* **Return type:**
  *List*[*datetime*]

<a id="mlserver.codecs.PandasCodec"></a>

### *class* mlserver.codecs.PandasCodec

Decodes a request (response) into a Pandas DataFrame, assuming each input
(output) head corresponds to a column of the DataFrame.

<a id="mlserver.codecs.PandasCodec.TypeHint"></a>

#### TypeHint

alias of `DataFrame`

<a id="mlserver.codecs.PandasCodec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.PandasCodec.encode_response"></a>

#### *classmethod* encode_response(model_name, payload, model_version=None, use_bytes=True, \*\*kwargs)

Encode the given payload into an inference response.

* **Parameters:**
  * **model_name** (*str*)
  * **payload** (*DataFrame*)
  * **model_version** (*str* *|* *None*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*InferenceResponse*](types.md#mlserver.types.InferenceResponse)

<a id="mlserver.codecs.PandasCodec.decode_response"></a>

#### *classmethod* decode_response(response)

Decode an inference response into a high-level Python object.

* **Parameters:**
  **response** ([*InferenceResponse*](types.md#mlserver.types.InferenceResponse))
* **Return type:**
  *DataFrame*

<a id="mlserver.codecs.PandasCodec.encode_request"></a>

#### *classmethod* encode_request(payload, use_bytes=True, \*\*kwargs)

Encode the given payload into an inference request.

* **Parameters:**
  * **payload** (*DataFrame*)
  * **use_bytes** (*bool*)
* **Return type:**
  [*InferenceRequest*](types.md#mlserver.types.InferenceRequest)

<a id="mlserver.codecs.PandasCodec.decode_request"></a>

#### *classmethod* decode_request(request)

Decode an inference request into a high-level Python object.

* **Parameters:**
  **request** ([*InferenceRequest*](types.md#mlserver.types.InferenceRequest))
* **Return type:**
  *DataFrame*
