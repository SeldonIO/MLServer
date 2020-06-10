from google.protobuf import json_format
from mlserver import types
from mlserver.grpc.converters import (
    ModelInferRequestConverter,
    ModelInferResponseConverter,
)
from mlserver.grpc import dataplane_pb2 as pb


def test_modelinferrequest_to_types(model_infer_request):
    inference_request = ModelInferRequestConverter.to_types(model_infer_request)

    expected = types.InferenceRequest(
        id="",
        inputs=[
            types.RequestInput(
                name="input-0",
                datatype="INT32",
                shape=[3],
                data=types.TensorData.parse_obj([1, 2, 3]),
            ),
            types.RequestInput(
                name="input-1",
                datatype="INT32",
                shape=[1],
                data=types.TensorData.parse_obj([4]),
            ),
            types.RequestInput(
                name="input-2",
                datatype="INT32",
                shape=[2],
                data=types.TensorData.parse_obj([5, 6]),
            ),
        ],
    )

    assert type(inference_request) is types.InferenceRequest
    assert dict(inference_request) == dict(expected)


def test_modelinferresponse_from_types(inference_response):
    model_infer_response = ModelInferResponseConverter.from_types(inference_response)

    expected = pb.ModelInferResponse(
        model_name="sum-model",
        id="123",
        outputs=[
            pb.ModelInferResponse.InferOutputTensor(
                name="output-0",
                datatype="FP32",
                shape=[1],
                contents=pb.InferTensorContents(fp32_contents=[21.0]),
            )
        ],
    )

    assert type(model_infer_response) is pb.ModelInferResponse
    assert json_format.MessageToDict(model_infer_response) == json_format.MessageToDict(
        expected
    )
