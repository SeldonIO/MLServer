import pytest
import numpy as np

from typing import Tuple, List

from mlflow.types.schema import ColSpec, TensorSpec, DataType
from mlserver.codecs import NumpyCodec, StringCodec, Base64Codec
from mlserver.types import Tags

from mlserver_mlflow.metadata import (
    InputSpec,
    _get_content_type,
    _get_shape,
    to_metadata_tensor,
)


@pytest.mark.parametrize(
    "input_spec, expected",
    [
        (
            TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
            ("INT32", NumpyCodec.ContentType),
        ),
        (
            ColSpec(name="foo", type=DataType.string),
            ("BYTES", StringCodec.ContentType),
        ),
        (
            ColSpec(name="foo", type=DataType.binary),
            ("BYTES", Base64Codec.ContentType),
        ),
    ],
)
def test_get_content_type(input_spec: InputSpec, expected: Tuple[str, str]):
    datatype, content_type = _get_content_type(input_spec)
    assert (datatype, content_type) == expected


@pytest.mark.parametrize(
    "input_spec, expected",
    [
        (
            TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
            [2, 2],
        ),
        (
            ColSpec(name="foo", type=DataType.string),
            [-1],
        ),
    ],
)
def test_get_shape(input_spec: InputSpec, expected: List[int]):
    shape = _get_shape(input_spec)
    assert shape == expected


def test_to_metadata_tensor():
    input_spec = TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32"))
    metadata_tensor = to_metadata_tensor(input_spec)

    assert metadata_tensor.name == input_spec.name
    assert metadata_tensor.datatype == "INT32"
    assert metadata_tensor.shape == list(input_spec.shape)
    assert metadata_tensor.tags == Tags(content_type=NumpyCodec.ContentType)
