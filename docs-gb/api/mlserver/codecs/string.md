# Module `mlserver.codecs.string`


## Class `StringCodec`


**Description:**
Encodes a list of Python strings as a BYTES input (output).

## Class `StringRequestCodec`


**Description:**
Decodes the first input (output) of request (response) as a list of
strings.
This codec can be useful for cases where the whole payload is a single
list of strings.

## Function `decode_str`


**Signature:** `decode_str(encoded: Union[bytes, str], str_codec='utf-8') -> str`


**Description:**
*No docstring available.*

## Function `encode_str`


**Signature:** `encode_str(elem: str) -> bytes`


**Description:**
*No docstring available.*
