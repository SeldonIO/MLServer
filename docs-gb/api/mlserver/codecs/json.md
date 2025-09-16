# Module `mlserver.codecs.json`


## Class `JSONEncoderWithArray`


**Description:**
Extensible JSON <https://json.org> encoder for Python data structures.
Supports the following objects and types by default:

+-------------------+---------------+
| Python            | JSON          |
+===================+===============+
| dict              | object        |
+-------------------+---------------+
| list, tuple       | array         |
+-------------------+---------------+
| str               | string        |
+-------------------+---------------+
| int, float        | number        |
+-------------------+---------------+
| True              | true          |
+-------------------+---------------+
| False             | false         |
+-------------------+---------------+
| None              | null          |
+-------------------+---------------+

To extend this to recognize other objects, subclass and implement a
``.default()`` method with another method that returns a serializable
object for ``o`` if possible, otherwise it should call the superclass
implementation (to raise ``TypeError``).

### Method `default`


**Signature:** `default(self, obj)`


**Description:**
Implement this method in a subclass such that it returns
a serializable object for ``o``, or calls the base implementation
(to raise a ``TypeError``).

For example, to support arbitrary iterators, you could
implement default like this::

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        # Let the base class default method raise the TypeError
        return super().default(o)

### Method `encode`


**Signature:** `encode(self, o)`


**Description:**
Return a JSON string representation of a Python data structure.
>>> from json.encoder import JSONEncoder
>>> JSONEncoder().encode({"foo": ["bar", "baz"]})
'{"foo": ["bar", "baz"]}'

### Method `iterencode`


**Signature:** `iterencode(self, o, _one_shot=False)`


**Description:**
Encode the given object and yield each string
representation as available.

For example::

    for chunk in JSONEncoder().iterencode(bigobject):
        mysocket.write(chunk)

## Function `decode_from_bytelike_json_to_dict`


**Signature:** `decode_from_bytelike_json_to_dict(v: Union[bytes, str]) -> dict`


**Description:**
*No docstring available.*

## Function `decode_json_input_or_output`


**Signature:** `decode_json_input_or_output(input_or_output: Union[mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.ResponseOutput]) -> List[Any]`


**Description:**
*No docstring available.*

## Function `encode_to_json`


**Signature:** `encode_to_json(v: Any, use_bytes: bool = True) -> Union[str, bytes]`


**Description:**
*No docstring available.*

## Function `encode_to_json_bytes`


**Signature:** `encode_to_json_bytes(v: Any) -> bytes`


**Description:**
encodes a dict into json bytes, can deal with byte like values gracefully
