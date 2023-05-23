import pytest

from datetime import datetime
from typing import Any

from mlserver.codecs import DatetimeCodec
from mlserver.types import RequestInput, ResponseOutput, Parameters

TestDatetimeIso = "2021-08-24T15:01:19"
TestDatetimeIsoB = b"2021-08-24T15:01:19"
TestDatetime = datetime.fromisoformat(TestDatetimeIso)

TestTzDatetimeIso = "2021-08-24T15:01:19-04:00"
TestTzDatetimeIsoB = b"2021-08-24T15:01:19-04:00"
TestTzDatetime = datetime.fromisoformat(TestTzDatetimeIso)


@pytest.mark.parametrize(
    "payload, expected",
    [
        ([TestDatetime, TestTzDatetime], True),
        ([TestDatetime, TestDatetimeIso], False),
        (TestDatetime, False),
    ],
)
def test_can_encode(payload: Any, expected: bool):
    assert DatetimeCodec.can_encode(payload) == expected


@pytest.mark.parametrize(
    "decoded, use_bytes, expected",
    [
        (
            # Single Python datetime object
            [TestDatetime],
            True,
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Multiple Python datetime objects
            [TestDatetime, TestDatetime],
            True,
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB, TestDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Single ISO-encoded string
            [TestDatetimeIso],
            True,
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Single Python datetime object with timezone
            [TestTzDatetime],
            True,
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestTzDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Single Python datetime object with timezone, but not using bytes
            [TestTzDatetime],
            False,
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestTzDatetimeIso],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
    ],
)
def test_encode_output(decoded, use_bytes, expected):
    response_output = DatetimeCodec.encode_output(
        name="foo", payload=decoded, use_bytes=use_bytes
    )

    assert expected == response_output


@pytest.mark.parametrize(
    "encoded, expected",
    [
        (
            # Single binary ISO-encoded datetime
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=TestDatetimeIsoB,
            ),
            [TestDatetime],
        ),
        (
            # Single (non-binary) ISO-encoded datetime
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestDatetimeIso],
            ),
            [TestDatetime],
        ),
        (
            # Multiple binary ISO-encoded datetime
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB, TestDatetimeIsoB],
            ),
            [TestDatetime, TestDatetime],
        ),
        (
            # Multiple (non-binary) ISO-encoded datetime
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[TestDatetimeIso, TestDatetimeIso],
            ),
            [TestDatetime, TestDatetime],
        ),
        (
            # Single (non-binary) ISO-encoded datetime with timezone
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestTzDatetimeIso],
            ),
            [TestTzDatetime],
        ),
    ],
)
def test_decode_output(encoded, expected):
    decoded_output = DatetimeCodec.decode_output(encoded)

    assert expected == decoded_output


@pytest.mark.parametrize(
    "decoded, use_bytes, expected",
    [
        (
            # Single Python datetime object
            [TestDatetime],
            True,
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Multiple Python datetime objects
            [TestDatetime, TestDatetime],
            True,
            RequestInput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB, TestDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Single ISO-encoded string
            [TestDatetimeIso],
            True,
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Single Python datetime object with timezone
            [TestTzDatetime],
            True,
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestTzDatetimeIsoB],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
        (
            # Single Python datetime object with timezone, not using bytes
            [TestTzDatetime],
            False,
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestTzDatetimeIso],
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
            ),
        ),
    ],
)
def test_encode_input(decoded, use_bytes, expected):
    request_input = DatetimeCodec.encode_input(
        name="foo", payload=decoded, use_bytes=use_bytes
    )

    assert expected == request_input


@pytest.mark.parametrize(
    "encoded, expected",
    [
        (
            # Single binary ISO-encoded datetime
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=TestDatetimeIsoB,
            ),
            [TestDatetime],
        ),
        (
            # Single (non-binary) ISO-encoded datetime
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestDatetimeIso],
            ),
            [TestDatetime],
        ),
        (
            # Multiple binary ISO-encoded datetime
            RequestInput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[TestDatetimeIsoB, TestDatetimeIsoB],
            ),
            [TestDatetime, TestDatetime],
        ),
        (
            # Multiple (non-binary) ISO-encoded datetime
            RequestInput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[TestDatetimeIso, TestDatetimeIso],
            ),
            [TestDatetime, TestDatetime],
        ),
        (
            # Single (non-binary) ISO-encoded datetime with timezone
            RequestInput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[TestTzDatetimeIso],
            ),
            [TestTzDatetime],
        ),
    ],
)
def test_decode_input(encoded, expected):
    decoded_input = DatetimeCodec.decode_input(encoded)

    assert expected == decoded_input
