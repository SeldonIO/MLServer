# Module `mlserver.codecs.base`


## Class `InputCodec`


**Description:**
The InputCodec interface lets you define type conversions of your raw input
data to / from the Open Inference Protocol.
Note that this codec applies at the individual input (output) level.

For request-wide transformations (e.g. dataframes), use the
``RequestCodec`` interface instead.

## Class `RequestCodec`


**Description:**
The ``RequestCodec`` interface lets you define request-level conversions
between high-level Python types and the Open Inference Protocol.
This can be useful where the encoding of your payload encompases multiple
input heads (e.g. dataframes, where each column can be thought as a
separate input head).

For individual input-level encoding / decoding, use the ``InputCodec``
interface instead.

## Function `deprecated`


**Signature:** `deprecated(reason: str)`


**Description:**
*No docstring available.*

## Function `register_input_codec`


**Signature:** `register_input_codec(CodecKlass: Union[Type[ForwardRef('InputCodec')], ForwardRef('InputCodec')])`


**Description:**
*No docstring available.*

## Function `register_request_codec`


**Signature:** `register_request_codec(CodecKlass: Union[Type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec')])`


**Description:**
*No docstring available.*
