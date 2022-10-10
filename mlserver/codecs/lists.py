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
    if isinstance(payload, list):
        # If it's a list, assume list of strings
        yield from payload
    else:
        # If not a list, assume that it's a single element
        yield payload
