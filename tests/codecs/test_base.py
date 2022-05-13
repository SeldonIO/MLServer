import numpy as np

from mlserver.codecs.numpy import NumpyCodec
from mlserver.types import RequestInput


def test_deprecated_methods(caplog):
    request_input = RequestInput(
        name="foo", shape=[3], data=[1, 2, 3], datatype="INT32"
    )
    expected = np.array([1, 2, 3])

    decoded = NumpyCodec.decode(request_input)

    assert any(["DEPRECATED" in rec.message for rec in caplog.records])
    np.testing.assert_array_equal(decoded, expected)
