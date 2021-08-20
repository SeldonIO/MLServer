import pytest
import numpy as np

from typing import Tuple

from mlflow.types.schema import ColSpec, TensorSpec, DataType
from mlserver.codecs import NumpyCodec

from mlserver_mlflow.metadata import InputSpec, to_content_type


@pytest.mark.parametrize(
    "input_spec, expected",
    [
        (
            TensorSpec(type=np.dtype("int32"), shape=(2, 2), name="foo"),
            ("INT32", NumpyCodec.ContentType),
        )
    ],
)
def test_to_content_type(input_spec: InputSpec, expected: Tuple[str, str]):
    datatype, content_type = to_content_type(input_spec)
    assert (datatype, content_type) == expected
