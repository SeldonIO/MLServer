# Codecs — Interfaces

### *class* mlserver.codecs.InputCodec

Bases: `object`

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
`RequestCodec` interface instead.

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

#### *classmethod* encode_output(name, payload, \*\*kwargs)

Encode the given payload into a response output.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)
* **Return type:**
  [*ResponseOutput*](types.md#mlserver.types.ResponseOutput)

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))
* **Return type:**
  *Any*

#### *classmethod* encode_input(name, payload, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)
* **Return type:**
  [*RequestInput*](types.md#mlserver.types.RequestInput)

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))
* **Return type:**
  *Any*

### *class* mlserver.codecs.RequestCodec

Bases: `object`

The `RequestCodec` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the `InputCodec`
interface instead.

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  bool

#### *classmethod* encode_response(model_name, payload, model_version=None, \*\*kwargs)

Encode the given payload into an inference response.

* **Parameters:**
  * **model_name** (*str*)
  * **payload** (*Any*)
  * **model_version** (*str* *|* *None*)
* **Return type:**
  [*InferenceResponse*](types.md#mlserver.types.InferenceResponse)

#### *classmethod* decode_response(response)

Decode an inference response into a high-level Python object.

* **Parameters:**
  **response** ([*InferenceResponse*](types.md#mlserver.types.InferenceResponse))
* **Return type:**
  *Any*

#### *classmethod* encode_request(payload, \*\*kwargs)

Encode the given payload into an inference request.

* **Parameters:**
  **payload** (*Any*)
* **Return type:**
  [*InferenceRequest*](types.md#mlserver.types.InferenceRequest)

#### *classmethod* decode_request(request)

Decode an inference request into a high-level Python object.

* **Parameters:**
  **request** ([*InferenceRequest*](types.md#mlserver.types.InferenceRequest))
* **Return type:**
  *Any*
