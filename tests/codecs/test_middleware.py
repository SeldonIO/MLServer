import pytest
import numpy as np
import pandas as pd

from typing import Any

from mlserver.types import RequestInput, Parameters, InferenceRequest
from mlserver.codecs import NumpyCodec, StringCodec, PandasCodec
from mlserver.codecs.middleware import DecodedParameterName, codec_middleware
from mlserver.settings import ModelSettings


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                parameters=Parameters(content_type=PandasCodec.ContentType),
                inputs=[
                    RequestInput(
                        name="foo",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                        datatype="INT32",
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                ],
            ),
            pd.DataFrame({"foo": [[1, 2], [3, 4]]}),
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type=PandasCodec.ContentType),
                inputs=[
                    RequestInput(
                        name="foo",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                        datatype="INT32",
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                    RequestInput(
                        name="bar",
                        shape=[2, 3],
                        data=b"heyabc",
                        datatype="BYTES",
                        parameters=Parameters(content_type=StringCodec.ContentType),
                    ),
                ],
            ),
            pd.DataFrame({"foo": [[1, 2], [3, 4]], "bar": ["hey", "abc"]}),
        ),
    ],
)
def test_decode_request(
    sum_model_settings: ModelSettings, inference_request: InferenceRequest, expected
):
    decoded_request = codec_middleware(inference_request, sum_model_settings)
    decoded = getattr(decoded_request.parameters, DecodedParameterName)

    pd.testing.assert_frame_equal(decoded, expected)


@pytest.mark.parametrize(
    "request_input,expected",
    [
        (
            RequestInput(
                name="foo",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT32",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
            np.array([[1, 2], [3, 4]]),
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
            np.array([1, 2], dtype=np.float32),
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
            ),
            None,
        ),
        (
            RequestInput(
                name="foo",
                shape=[17],
                data=b"my unicode string",
                datatype="BYTES",
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
            ["my unicode string"],
        ),
        (
            # sum-model has metadata setting the default content type of input
            # `input-0` to `np`
            RequestInput(
                name="input-0",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT32",
            ),
            np.array([[1, 2], [3, 4]]),
        ),
    ],
)
def test_decode_request_inputs(
    sum_model_settings: ModelSettings, request_input: RequestInput, expected: Any
):
    request = InferenceRequest(inputs=[request_input])
    request = codec_middleware(request, sum_model_settings)

    if expected is None:
        assert not request.inputs[0].parameters
    else:
        decoded = getattr(request.inputs[0].parameters, DecodedParameterName)
        if isinstance(expected, np.ndarray):
            np.testing.assert_array_equal(decoded, expected)  # type: ignore
        else:
            assert decoded == expected  # type: ignore
