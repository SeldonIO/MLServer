from typing import Generator, Union, Iterable, List, Tuple


PackElement = Union[bytes, str]
PackedPayload = Union[PackElement, List[PackElement]]


def unpack(
    packed: PackedPayload, shape: List[int]
) -> Generator[PackElement, None, None]:
    if isinstance(packed, list):
        # If it's a list, assume list of strings
        yield from packed
    else:
        if len(shape) == 0:
            # If there is no shape, assume that it's a single element
            yield packed
        else:
            # Otherwise, assume content is a concatenated list of same-length
            # strings and get the common length from the shape
            common_length = shape[-1]
            for i in range(0, len(packed), common_length):
                yield packed[i : i + common_length]


def pack(unpacked: Iterable[bytes]) -> Tuple[PackedPayload, List[int]]:
    packed = b""
    common_length = -1
    N = 0
    for elem in unpacked:
        # TODO: Should we use the length of the UTF8 string or the bytes
        # array?
        elem_length = len(elem)
        if common_length == -1:
            common_length = elem_length

        if common_length != elem_length:
            # TODO: Raise an error here
            # TODO: Should we try to add padding?
            pass

        N += 1
        packed += elem

    shape = [N, common_length]
    return packed, shape
