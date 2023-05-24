import pytest
import numpy as np
import pandas as pd

from typing import Any

from mlserver.codecs import (
    InputCodec,
    RequestCodec,
    NumpyCodec,
    StringCodec,
    PandasCodec,
    Base64Codec,
    decode_inference_request,
)
from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc.converters import (
    ModelInferResponseConverter,
    ModelInferRequestConverter,
    InferOutputTensorConverter,
    InferInputTensorConverter,
)


@pytest.mark.parametrize(
    "decoded, codec, expected",
    [
        (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
            PandasCodec,
            pb.ModelInferResponse(
                model_name="my-model",
                parameters={
                    "content_type": pb.InferParameter(
                        string_param=PandasCodec.ContentType
                    )
                },
                outputs=[
                    pb.ModelInferResponse.InferOutputTensor(
                        name="a",
                        datatype="INT64",
                        shape=[3, 1],
                        contents=pb.InferTensorContents(int64_contents=[1, 2, 3]),
                    ),
                    pb.ModelInferResponse.InferOutputTensor(
                        name="b",
                        datatype="BYTES",
                        shape=[3, 1],
                        contents=pb.InferTensorContents(
                            bytes_contents=[b"A", b"B", b"C"]
                        ),
                        parameters={
                            "content_type": pb.InferParameter(
                                string_param=StringCodec.ContentType
                            )
                        },
                    ),
                ],
            ),
        )
    ],
)
def test_encode_infer_response(
    decoded: Any, codec: RequestCodec, expected: pb.ModelInferResponse
):
    inference_response = codec.encode_response("my-model", decoded)
    model_infer_response = ModelInferResponseConverter.from_types(inference_response)
    assert model_infer_response == expected


@pytest.mark.parametrize(
    "encoded, expected",
    [
        (
            pb.ModelInferRequest(
                parameters={"content_type": pb.InferParameter(string_param="pd")},
                inputs=[
                    pb.ModelInferRequest.InferInputTensor(
                        name="a",
                        datatype="INT64",
                        shape=[3],
                        contents=pb.InferTensorContents(int64_contents=[1, 2, 3]),
                    ),
                    pb.ModelInferRequest.InferInputTensor(
                        name="b",
                        datatype="BYTES",
                        shape=[3],
                        parameters={
                            "content_type": pb.InferParameter(string_param="str")
                        },
                        contents=pb.InferTensorContents(
                            bytes_contents=[b"A", b"B", b"C"]
                        ),
                    ),
                ],
            ),
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
        )
    ],
)
def test_decode_infer_request(encoded: pb.ModelInferRequest, expected: Any):
    inference_request = ModelInferRequestConverter.to_types(encoded)
    decoded = decode_inference_request(inference_request)
    pd.testing.assert_frame_equal(decoded, expected)


@pytest.mark.parametrize(
    "decoded, codec, expected",
    [
        (
            np.array([21.0]),
            NumpyCodec,
            pb.ModelInferResponse.InferOutputTensor(
                name="output-0",
                datatype="FP64",
                shape=[1, 1],
                contents=pb.InferTensorContents(fp64_contents=[21.0]),
                parameters={
                    "content_type": pb.InferParameter(
                        string_param=NumpyCodec.ContentType
                    )
                },
            ),
        ),
        (
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
            NumpyCodec,
            pb.ModelInferResponse.InferOutputTensor(
                name="output-0",
                datatype="BYTES",
                shape=[2, 1],
                contents=pb.InferTensorContents(bytes_contents=[b"\x01\x02"]),
                parameters={
                    "content_type": pb.InferParameter(
                        string_param=NumpyCodec.ContentType
                    )
                },
            ),
        ),
        (
            ["hey", "what's", "up"],
            StringCodec,
            pb.ModelInferResponse.InferOutputTensor(
                name="output-0",
                datatype="BYTES",
                shape=[3, 1],
                parameters={
                    "content_type": pb.InferParameter(
                        string_param=StringCodec.ContentType
                    )
                },
                contents=pb.InferTensorContents(
                    bytes_contents=[b"hey", b"what's", b"up"]
                ),
            ),
        ),
        (
            [b"Python is fun"],
            Base64Codec,
            pb.ModelInferResponse.InferOutputTensor(
                name="output-0",
                datatype="BYTES",
                shape=[1, 1],
                contents=pb.InferTensorContents(
                    bytes_contents=[b"UHl0aG9uIGlzIGZ1bg=="]
                ),
                parameters={
                    "content_type": pb.InferParameter(
                        string_param=Base64Codec.ContentType
                    )
                },
            ),
        ),
    ],
)
def test_encode_output_tensor(
    decoded: Any, codec: InputCodec, expected: pb.ModelInferResponse.InferOutputTensor
):
    response_output = codec.encode_output(name="output-0", payload=decoded)
    infer_output_tensor = InferOutputTensorConverter.from_types(response_output)
    assert infer_output_tensor == expected


@pytest.mark.parametrize(
    "encoded, codec, expected",
    [
        (
            pb.ModelInferRequest.InferInputTensor(
                name="output-0",
                datatype="FP64",
                shape=[1],
                contents=pb.InferTensorContents(fp64_contents=[21.0]),
            ),
            NumpyCodec,
            np.array([21.0]),
        ),
        (
            pb.ModelInferRequest.InferInputTensor(
                name="output-0",
                datatype="BYTES",
                shape=[3],
                contents=pb.InferTensorContents(
                    bytes_contents=[b"hey", b"what's", b"up"]
                ),
            ),
            StringCodec,
            ["hey", "what's", "up"],
        ),
    ],
)
def test_decode_input_tensor(
    encoded: pb.ModelInferRequest.InferInputTensor, codec: InputCodec, expected: Any
):
    request_input = InferInputTensorConverter.to_types(encoded)
    decoded = codec.decode_input(request_input)
    assert decoded == expected
