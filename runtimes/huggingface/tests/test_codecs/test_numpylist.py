# mypy: disable-error-code="arg-type"

import pytest
import numpy as np
from mlserver.types import RequestInput, ResponseOutput, Parameters, TensorData
from mlserver_huggingface.codecs import NumpyListCodec


@pytest.mark.parametrize(
    "name, var, expected1, expected2",
    [
        (
            "float64",
            [np.zeros([1, 2]), np.zeros([1, 2])],
            True,
            RequestInput(
                name="float64",
                shape=[2, 1, 2],
                datatype="FP64",
                parameters=Parameters(content_type="nplist"),
                data=TensorData(root=[0.0, 0.0, 0.0, 0.0]),
            ),
        ),
        (
            "int8",
            [np.int8([[1, 2]]), np.int8([[1, 2]])],
            True,
            RequestInput(
                name="int8",
                datatype="INT8",
                data=TensorData(root=[1, 2, 1, 2]),
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
        ),
        (
            "mixdtype",
            [np.int8([[1, 2]]), np.zeros([1, 2])],
            True,
            RequestInput(
                name="mixdtype",
                datatype="FP64",
                data=TensorData(root=[1, 2, 0.0, 0.0]),
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
        ),
        ("diffrentshape", [np.int8([[1, 2]]), np.zeros([2, 2])], False, None),
    ],
)
def test_encode_input(name, var, expected1, expected2):
    can_encode = NumpyListCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert NumpyListCodec.encode_input(name, var) == expected2


@pytest.mark.parametrize(
    "req, expected",
    [
        (
            RequestInput(
                name="float64",
                shape=[2, 1, 2],
                datatype="FP64",
                data=TensorData(root=[0.0, 0.0, 0.0, 0.0]),
                parameters=Parameters(content_type="nplist"),
            ),
            [np.zeros([1, 2]), np.zeros([1, 2])],
        ),
        (
            RequestInput(
                name="int8",
                datatype="INT8",
                data=TensorData(root=[1, 2, 1, 2]),
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
            [np.int8([[1, 2]]), np.int8([[1, 2]])],
        ),
        (
            RequestInput(
                name="mixdtype",
                datatype="FP64",
                data=TensorData(root=[1, 2, 0.0, 0.0]),
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
            [np.float64([[1, 2]]), np.zeros([1, 2])],
        ),
    ],
)
def test_decode_input(req, expected):
    decoded = NumpyListCodec.decode_input(req)
    assert np.array_equal(decoded, expected)


@pytest.mark.parametrize(
    "name, var, expected",
    [
        (
            "float64",
            [np.zeros([1, 2]), np.zeros([1, 2])],
            ResponseOutput(
                name="float64",
                shape=[2, 1, 2],
                datatype="FP64",
                data=[0.0, 0.0, 0.0, 0.0],
                parameters=Parameters(content_type="nplist"),
            ),
        ),
        (
            "int8",
            [np.int8([[1, 2]]), np.int8([[1, 2]])],
            ResponseOutput(
                name="int8",
                datatype="INT8",
                data=[1, 2, 1, 2],
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
        ),
        (
            "mixdtype",
            [np.int8([[1, 2]]), np.zeros([1, 2])],
            ResponseOutput(
                name="mixdtype",
                datatype="FP64",
                data=[1, 2, 0.0, 0.0],
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
        ),
    ],
)
def test_encode_output(name, var, expected):
    assert NumpyListCodec.encode_output(name, var) == expected


@pytest.mark.parametrize(
    "out, expected",
    [
        (
            ResponseOutput(
                name="float64",
                shape=[2, 1, 2],
                datatype="FP64",
                data=[0.0, 0.0, 0.0, 0.0],
                parameters=Parameters(content_type="nplist"),
            ),
            [np.zeros([1, 2]), np.zeros([1, 2])],
        ),
        (
            ResponseOutput(
                name="int8",
                datatype="INT8",
                data=[1, 2, 1, 2],
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
            [np.int8([[1, 2]]), np.int8([[1, 2]])],
        ),
        (
            ResponseOutput(
                name="mixdtype",
                datatype="FP64",
                data=[1, 2, 0.0, 0.0],
                parameters=Parameters(content_type="nplist"),
                shape=[2, 1, 2],
            ),
            [np.float64([[1, 2]]), np.zeros([1, 2])],
        ),
    ],
)
def test_decode_output(out, expected):
    decoded = NumpyListCodec.decode_output(out)
    for idx, el in enumerate(decoded):
        assert el.dtype == expected[idx].dtype
    assert np.array_equal(NumpyListCodec.decode_output(out), expected)
