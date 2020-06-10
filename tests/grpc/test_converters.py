from mlserver import types
from mlserver.grpc.converters import ModelInferRequestConverter
from mlserver.grpc import dataplane_pb2 as pb

from .utils import read_testdata_pb


def test_modelinferrequest_to_types():
    model_infer_request = read_testdata_pb(
        "model-infer-request.json", pb.ModelInferRequest
    )
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
