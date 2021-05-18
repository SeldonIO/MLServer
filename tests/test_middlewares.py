import pytest
import numpy as np

from typing import Any, List

from mlserver.types import InferenceRequest, RequestInput, Parameters
from mlserver.middlewares import content_type_middleware
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.model import MLModel


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
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
                RequestInput(
                    name="bar",
                    shape=[2],
                    data=[1, 2],
                    datatype="FP32",
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
            ],
            [np.array([[1, 2], [3, 4]]), np.array([1, 2], dtype=np.float32)],
        ),
        (
            [
                RequestInput(
                    name="foo",
                    shape=[2, 2],
                    data=[1, 2, 3, 4],
                    datatype="INT32",
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
                RequestInput(
                    name="bar",
                    shape=[2],
                    data=[1, 2],
                    datatype="FP32",
                ),
            ],
            [np.array([[1, 2], [3, 4]]), None],
        ),
        (
            [
                RequestInput(
                    name="foo",
                    shape=[17],
                    data=b"my unicode string",
                    datatype="BYTES",
                    parameters=Parameters(content_type=StringCodec.ContentType),
                )
            ],
            ["my unicode string"],
        ),
        (
            # sum-model has metadata setting the default content type to `np`
            [
                RequestInput(
                    name="foo",
                    shape=[2, 2],
                    data=[1, 2, 3, 4],
                    datatype="INT32",
                ),
            ],
            [np.array([[1, 2], [3, 4]])],
        ),
    ],
)
def test_content_type_middleware(
    sum_model: MLModel, inputs: List[RequestInput], decoded: List[Any]
):
    request = InferenceRequest(inputs=inputs)
    decoded_request = content_type_middleware(request, sum_model)

    for inp, dec in zip(decoded_request.inputs, decoded):
        params = inp.parameters
        if not params:
            continue

        if dec is None:
            assert not params.decoded_content

        if params.content_type == "np":
            np.testing.assert_array_equal(params.decoded_content, dec)  # type: ignore
        else:
            assert params.decoded_content == dec  # type: ignore
