import pytest

from mlserver.types import RequestInput, ResponseOutput, Parameters, TensorData
from mlserver_huggingface.codecs import RawCodec


@pytest.mark.parametrize(
    "input_name, input_var, expected1, expected2",
    [
        (
            "foo1",
            "bar1",
            True,
            RequestInput(
                name="foo1",
                datatype="BYTES",
                data=TensorData(root=["bar1"]),
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
        ),
        (
            "foo2",
            1,
            True,
            RequestInput(
                name="foo2",
                datatype="BYTES",
                data=TensorData(root=[1]),
                parameters=Parameters(content_type="raw"),
                shape=[1],
            ),
        ),
        (
            "foo3",
            1.0,
            True,
            RequestInput(
                name="foo3",
                datatype="BYTES",
                data=TensorData(root=[1.0]),
                parameters=Parameters(content_type="raw"),
                shape=[1],
            ),
        ),
        ("foo3", [], False, None),
    ],
)
def test_encode_input(input_name, input_var, expected1, expected2):
    can_encode = RawCodec.can_encode(input_var)
    assert can_encode == expected1
    if can_encode:
        assert RawCodec.encode_input(input_name, input_var) == expected2


@pytest.mark.parametrize(
    "request_input, expected",
    [
        (
            RequestInput(
                name="foo",
                datatype="BYTES",
                data=["bar1", "bar2"],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
            "bar1",
        ),
        (
            RequestInput(
                name="foo2",
                datatype="BYTES",
                data=[1],
                shape=[1],
                Parameters=Parameters(content_type="raw"),
            ),
            1,
        ),
        (
            RequestInput(
                name="foo2",
                datatype="BYTES",
                data=[1.0],
                shape=[1],
                Parameters=Parameters(content_type="raw"),
            ),
            1.0,
        ),
    ],
)
def test_decode_input(request_input, expected):
    decoded = RawCodec.decode_input(request_input)
    assert decoded == expected


@pytest.mark.parametrize(
    "name, var, expected",
    [
        (
            "foo",
            1,
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                data=[1],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
        ),
        (
            "foo",
            "foo",
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                data=["foo"],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
        ),
        (
            "foo",
            0.1,
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                data=[0.1],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
        ),
    ],
)
def test_encode_output(name, var, expected):
    assert RawCodec.encode_output(name, var) == expected


@pytest.mark.parametrize(
    "out, expected",
    [
        (
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                data=[1],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
            1,
        ),
        (
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                data=["foo"],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
            "foo",
        ),
        (
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                data=[0.1],
                shape=[1],
                parameters=Parameters(content_type="raw"),
            ),
            0.1,
        ),
    ],
)
def test_decode_output(out, expected):
    assert RawCodec.decode_output(out) == expected
