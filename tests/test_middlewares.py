import pytest
import numpy as np

from typing import Any, List

from mlserver.types import InferenceRequest, RequestInput
from mlserver.middlewares import ContentTypeKey, content_type_middleware
from mlserver.codecs import NumpyCodec


@pytest.mark.parametrize(
    "inputs,decoded",
    [
        (
            [
                RequestInput(
                    name="foo",
                    shape=[2, 2],
                    data=[1, 2, 3, 4],
                    datatype="INT32",
                    parameters={ContentTypeKey: NumpyCodec.ContentType},
                ),
            ],
            [np.array([[1, 2], [3, 4]])],
        )
    ],
)
def test_content_type_middleware(inputs: List[RequestInput], decoded: List[Any]):
    request = InferenceRequest(inputs=inputs)
    decoded_request = content_type_middleware(request)
    breakpoint()

    assert decoded_request
