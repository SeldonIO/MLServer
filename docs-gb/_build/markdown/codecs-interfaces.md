# Codecs — Interfaces

### *class* mlserver.codecs.InputCodec

Bases: `object`

The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
`RequestCodec` interface instead.

#### ContentType *: `typing.ClassVar`[`str`]* *= ''*

#### TypeHint

alias of `None`

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Return type:**
  `bool`
* **Parameters:**
  **payload** (*Any*)

#### *classmethod* encode(cls, name, payload)

* **Return type:**
  [`mlserver.types.dataplane.ResponseOutput`](types.md#mlserver.types.ResponseOutput)
* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)

#### *classmethod* encode_output(name, payload, \*\*kwargs)

Encode the given payload into a response output.

* **Return type:**
  [`mlserver.types.dataplane.ResponseOutput`](types.md#mlserver.types.ResponseOutput)
* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)

#### *classmethod* decode_output(response_output)

Decode a response output into a high-level Python type.

* **Return type:**
  `typing.Any`
* **Parameters:**
  **response_output** ([*ResponseOutput*](types.md#mlserver.types.ResponseOutput))

#### *classmethod* encode_input(name, payload, \*\*kwargs)

Encode the given payload into a `RequestInput`.

* **Return type:**
  [`mlserver.types.dataplane.RequestInput`](types.md#mlserver.types.RequestInput)
* **Parameters:**
  * **name** (*str*)
  * **payload** (*Any*)

#### *classmethod* decode(cls, request_input)

* **Return type:**
  `typing.Any`
* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))

#### *classmethod* decode_input(request_input)

Decode a request input into a high-level Python type.

* **Return type:**
  `typing.Any`
* **Parameters:**
  **request_input** ([*RequestInput*](types.md#mlserver.types.RequestInput))

### *class* mlserver.codecs.RequestCodec

Bases: `object`

The `RequestCodec` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the `InputCodec`
interface instead.

#### ContentType *: `typing.ClassVar`[`str`]* *= ''*

#### TypeHint

alias of `None`

#### *classmethod* can_encode(payload)

Evaluate whether the codec can encode (decode) the payload.

* **Return type:**
  `bool`
* **Parameters:**
  **payload** (*Any*)

#### *classmethod* encode(cls, model_name, payload, model_version=None)

* **Return type:**
  [`mlserver.types.dataplane.InferenceResponse`](types.md#mlserver.types.InferenceResponse)
* **Parameters:**
  * **model_name** (*str*)
  * **payload** (*Any*)
  * **model_version** (*str* *|* *None*)

#### *classmethod* encode_response(model_name, payload, model_version=None, \*\*kwargs)

Encode the given payload into an inference response.

* **Return type:**
  [`mlserver.types.dataplane.InferenceResponse`](types.md#mlserver.types.InferenceResponse)
* **Parameters:**
  * **model_name** (*str*)
  * **payload** (*Any*)
  * **model_version** (*str* *|* *None*)

#### *classmethod* decode_response(response)

Decode an inference response into a high-level Python object.

* **Return type:**
  `typing.Any`
* **Parameters:**
  **response** ([*InferenceResponse*](types.md#mlserver.types.InferenceResponse))

#### *classmethod* encode_request(payload, \*\*kwargs)

Encode the given payload into an inference request.

* **Return type:**
  [`mlserver.types.dataplane.InferenceRequest`](types.md#mlserver.types.InferenceRequest)
* **Parameters:**
  **payload** (*Any*)

#### *classmethod* decode(cls, request)

* **Return type:**
  `typing.Any`
* **Parameters:**
  **request** ([*InferenceRequest*](types.md#mlserver.types.InferenceRequest))

#### *classmethod* decode_request(request)

Decode an inference request into a high-level Python object.

* **Return type:**
  `typing.Any`
* **Parameters:**
  **request** ([*InferenceRequest*](types.md#mlserver.types.InferenceRequest))
