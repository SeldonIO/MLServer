import pytest

from typing import Dict, Tuple

from mlserver.grpc.utils import to_metadata


@pytest.mark.parametrize(
    "headers, expected",
    [
        ({"foo": "bar"}, (("foo", "bar"),)),
        ({"foo": "bar", "foo2": "bar2"}, (("foo", "bar"), ("foo2", "bar2"))),
        ({"foo": "bar", "X-Foo": "bar2"}, (("foo", "bar"), ("x-foo", "bar2"))),
    ],
)
def test_to_metadata(headers: Dict[str, str], expected: Tuple[Tuple[str, str], ...]):
    metadata = to_metadata(headers)

    assert metadata == expected
