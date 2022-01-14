import pytest

from mlserver.types import ResponseOutput

from mlserver_alibi_explain.common import convert_from_bytes
from mlserver_alibi_explain.errors import InvalidExplanationShape


@pytest.mark.parametrize(
    "output",
    [
        ResponseOutput(name="foo", datatype="INT32", shape=[1, 1], data=[1]),
        ResponseOutput(name="foo", datatype="INT32", shape=[1, 2], data=[1, 2]),
    ],
)
def test_convert_from_bytes_invalid(output: ResponseOutput):
    with pytest.raises(InvalidExplanationShape):
        convert_from_bytes(output)
