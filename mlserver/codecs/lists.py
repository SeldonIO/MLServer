"""
Utils to work transparently with either lists of strings, or single strings.
"""

from typing import Any, Type, Union, List, Iterator

ListElement = Union[bytes, str]
ListPayload = Union[ListElement, List[ListElement]]


def is_list_of(payload: Any, instance_type: Type):
    if not isinstance(payload, list):
        return False

    def isinstance_of_type(payload: Any) -> bool:
        return isinstance(payload, instance_type)

    return all(map(isinstance_of_type, payload))


def as_list(payload: ListPayload) -> Iterator[ListElement]:
    """Return a payload as an iterator. Single elements will be
    treated as a list of 1 item. All elements are assumed to be
    string-like."""
    if isinstance(payload, list):
        yield from payload
    else:
        yield payload
