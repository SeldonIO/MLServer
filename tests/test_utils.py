import pytest
import numpy as np

from mlserver.utils import to_datatype


@pytest.mark.parametrize(
    "dtype, datatype",
    [
        (np.bool_, "BOOL"),
        (np.uint8, "UINT8"),
        (np.uint16, "UINT16"),
        (np.uint32, "UINT32"),
        (np.uint64, "UINT64"),
        (np.int8, "INT8"),
        (np.int16, "INT16"),
        (np.int32, "INT32"),
        (np.int64, "INT64"),
        (np.float16, "FP16"),
        (np.float32, "FP32"),
        (np.float64, "FP64"),
        (np.byte, "INT8"),
    ],
)
def test_to_datatype(dtype, datatype):
    dtype = np.dtype(dtype)

    obtained_datatype = to_datatype(dtype)
    assert datatype == obtained_datatype
