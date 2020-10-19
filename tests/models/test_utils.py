import pytest

from mlserver.types import RequestInput, TensorData
from mlserver.models import _NUMPY_PRESENT
from mlserver.models.utils import NP_DTYPES, to_dtype, to_ndarray

from .helpers import skipif_numpy_missing

if _NUMPY_PRESENT:
    import numpy as np


@skipif_numpy_missing
@pytest.mark.parametrize("datatype, expected", NP_DTYPES.items())
def test_to_dtype(datatype, expected):
    expected_dtype = np.dtype(expected)
    dtype = to_dtype(datatype)
    assert dtype == expected_dtype


@skipif_numpy_missing
@pytest.mark.parametrize(
    "request_input,expected",
    [
        (
            RequestInput(
                name="input-0",
                data=TensorData.parse_obj([1, 2, 3]),
                shape=[3],
                datatype="INT32",
            ),
            dict(object=[1, 2, 3], dtype="int32"),
        ),
        (
            RequestInput(
                name="input-0",
                data=TensorData.parse_obj([1, 2, 3]),
                shape=[1, 3],
                datatype="INT32",
            ),
            dict(object=[[1, 2, 3]], dtype="int32"),
        ),
        (
            RequestInput(
                name="input-0",
                data=TensorData.parse_obj([1.4, 2.3, 3.1, 4.5]),
                shape=[2, 2],
                datatype="FP32",
            ),
            dict(object=[[1.4, 2.3], [3.1, 4.5]], dtype="float32"),
        ),
    ],
)
def test_to_ndarray(request_input, expected):
    expected_ndarray = np.array(**expected)
    ndarray = to_ndarray(request_input)
    assert np.array_equal(ndarray, expected_ndarray)
