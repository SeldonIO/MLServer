from typing import Generator, Union, List


PackElement = Union[bytes, str]
PackedPayload = Union[PackElement, List[PackElement]]


def unpack(packed: PackedPayload) -> Generator[PackElement, None, None]:
    if isinstance(packed, list):
        # If it's a list, assume list of strings
        yield from packed
    else:
        # If there is no shape, assume that it's a single element
        yield packed
