<a id="codecs-interfaces"></a>

# Codecs — Interfaces

<a id="mlserver.codecs.InputCodec"></a>

### *class* mlserver.codecs.InputCodec

Bases: `object`

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
`RequestCodec` interface instead.

<a id="mlserver.codecs.InputCodec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.InputCodec.encode_output"></a>

#### *classmethod* encode_output(name, payload, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

<a id="mlserver.codecs.InputCodec.decode_output"></a>

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))
* **Return type:**
  *Any*

<a id="mlserver.codecs.InputCodec.encode_input"></a>

#### *classmethod* encode_input(name, payload, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

<a id="mlserver.codecs.InputCodec.decode_input"></a>

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))
* **Return type:**
  *Any*

<a id="mlserver.codecs.RequestCodec"></a>

### *class* mlserver.codecs.RequestCodec

Bases: `object`

The `RequestCodec` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the `InputCodec`
interface instead.

<a id="mlserver.codecs.RequestCodec.can_encode"></a>

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

<a id="mlserver.codecs.RequestCodec.encode_response"></a>

#### *classmethod* encode_response(model_name, payload, model_version=None, \*\*kwargs)

Encode the given payload into an inference response.

* **Parameters:**
  * **model_name** (*str*)
  * **payload** (*Any*)
  * **model_version** (*str* *|* *None*)
* **Return type:**
  [*InferenceResponse*](types.md#mlserver.types.InferenceResponse)

<a id="mlserver.codecs.RequestCodec.decode_response"></a>

#### *classmethod* decode_response(response)

Decode an inference response into a high-level Python object.

* **Parameters:**
  **response** ([*InferenceResponse*](types.md#mlserver.types.InferenceResponse))
* **Return type:**
  *Any*

<a id="mlserver.codecs.RequestCodec.encode_request"></a>

#### *classmethod* encode_request(payload, \*\*kwargs)

Encode the given payload into an inference request.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  [*InferenceRequest*](types.md#mlserver.types.InferenceRequest)

<a id="mlserver.codecs.RequestCodec.decode_request"></a>

#### *classmethod* decode_request(request)

Decode an inference request into a high-level Python object.

* **Parameters:**
  **request** ([*InferenceRequest*](types.md#mlserver.types.InferenceRequest))
* **Return type:**
  *Any*
