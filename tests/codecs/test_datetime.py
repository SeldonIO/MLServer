import pytest

from datetime import datetime

from mlserver.codecs import DatetimeCodec
from mlserver.types import RequestInput, ResponseOutput

TestDatetimeIso = "2021-08-24T15:01:19"
TestDatetimeIsoB = b"2021-08-24T15:01:19"
TestDatetime = datetime.fromisoformat(TestDatetimeIso)

TestTzDatetimeIso = "2021-08-24T15:01:19-04:00"
TestTzDatetimeIsoB = b"2021-08-24T15:01:19-04:00"
TestTzDatetime = datetime.fromisoformat(TestTzDatetimeIso)


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            [TestDatetime],
            ResponseOutput(
                name="foo",
                shape=[1, 19],
                datatype="BYTES",
                data=TestDatetimeIsoB,
            ),
        ),
        (
            [TestDatetime, TestDatetime],
            ResponseOutput(
                name="foo",
                shape=[2, 19],
                datatype="BYTES",
                data=TestDatetimeIsoB + TestDatetimeIsoB,
            ),
        ),
        (
            [TestDatetimeIso],
            ResponseOutput(
                name="foo",
                shape=[1, 19],
                datatype="BYTES",
                data=TestDatetimeIsoB,
            ),
        ),
        (
            [TestTzDatetime],
            ResponseOutput(
                name="foo",
                shape=[1, 25],
                datatype="BYTES",
                data=TestTzDatetimeIsoB,
            ),
        ),
    ],
)
def test_encode(decoded, expected):
    codec = DatetimeCodec()
    response_output = codec.encode(name="foo", payload=decoded)

    assert expected == response_output


@pytest.mark.parametrize(
    "encoded, expected",
    [
        (
            RequestInput(
                name="foo",
                shape=[1, 19],
                datatype="BYTES",
                data=TestDatetimeIsoB,
            ),
            [TestDatetime],
        ),
        (
            RequestInput(
                name="foo",
                shape=[1, 19],
                datatype="BYTES",
                data=TestDatetimeIso,
            ),
            [TestDatetime],
        ),
        (
            RequestInput(
                name="foo",
                shape=[1, 19],
                datatype="BYTES",
                data=TestDatetimeIsoB + TestDatetimeIsoB,
            ),
            [TestDatetime, TestDatetime],
        ),
        (
            RequestInput(
                name="foo",
                shape=[1, 19],
                datatype="BYTES",
                data=TestDatetimeIso + TestDatetimeIso,
            ),
            [TestDatetime, TestDatetime],
        ),
        (
            RequestInput(
                name="foo",
                shape=[1, 25],
                datatype="BYTES",
                data=TestTzDatetimeIso,
            ),
            [TestTzDatetime],
        ),
    ],
)
def test_decode(encoded, expected):
    codec = DatetimeCodec()
    decoded_input = codec.decode(encoded)

    assert expected == decoded_input
