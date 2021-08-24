from typing import Any, Callable, Generator, Union, List, Tuple


PayloadElement = Union[bytes, str]
PackedPayload = Union[PayloadElement, List[PayloadElement]]
Encoder = Callable[[Any], bytes]
Decoder = Callable[[PayloadElement], Any]


def _split_elements(
    encoded: PackedPayload, shape: List[int]
) -> Generator[PayloadElement, None, None]:
    if isinstance(encoded, list):
        # If it's a list, assume list of strings
        yield from encoded
    elif isinstance(encoded, bytes):
        if len(shape) == 0:
            # If there is no shape, assume that it's a single element
            yield encoded
        else:
            # Otherwise, assume content is a concatenated list of same-length
            # strings and get the common length from the shape
            common_length = shape[-1]
            for i in range(0, len(encoded), common_length):
                yield encoded[i : i + common_length]
    elif isinstance(encoded, str):
        yield encoded


def unpack(
    packed: PackedPayload, shape: List[int], decoder: Decoder
) -> Generator[Any, None, None]:
    for elem in _split_elements(packed, shape):
        yield decoder(elem)


def pack(unpacked: List[Any], encoder: Encoder) -> Tuple[PackedPayload, List[int]]:
    packed = b""
    common_length = -1
    for elem in unpacked:
        as_bytes = encoder(elem)

        # TODO: Should we use the length of the UTF8 string or the bytes
        # array?
        elem_length = len(as_bytes)
        if common_length == -1:
            common_length = elem_length

        if common_length != elem_length:
            # TODO: Raise an error here
            # TODO: Should we try to add padding?
            pass

        packed += as_bytes

    shape = [len(unpacked), common_length]
    return packed, shape
