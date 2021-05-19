from google.protobuf import json_format
from mlserver import types
from mlserver.grpc.converters import (
    ModelInferRequestConverter,
    ModelInferResponseConverter,
    ServerMetadataResponseConverter,
    ModelMetadataResponseConverter,
    RepositoryIndexRequestConverter,
    RepositoryIndexResponseConverter,
    ParametersConverter,
)
from mlserver.grpc import dataplane_pb2 as pb


def test_servermetadataresponse_from_types(metadata_server_response):
    metadata = ServerMetadataResponseConverter.from_types(metadata_server_response)

    assert metadata.name == metadata_server_response.name
    assert metadata.version == metadata_server_response.version
    assert metadata.extensions == metadata_server_response.extensions


def test_modelmetadataresponse_from_types(metadata_model_response):
    metadata = ModelMetadataResponseConverter.from_types(metadata_model_response)

    assert metadata.name == metadata_model_response.name
    assert metadata.versions == metadata_model_response.versions
    assert metadata.platform == metadata_model_response.platform

    for pb_obj, ty_obj in zip(metadata.inputs, metadata_model_response.inputs):
        assert pb_obj.name == ty_obj.name
        assert pb_obj.datatype == ty_obj.datatype
        assert pb_obj.shape == ty_obj.shape

    for pb_obj, ty_obj in zip(metadata.outputs, metadata_model_response.outputs):
        assert pb_obj.name == ty_obj.name
        assert pb_obj.datatype == ty_obj.datatype
        assert pb_obj.shape == ty_obj.shape


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
                parameters=types.Parameters(content_type="np"),
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


def test_repositoryindexrequest_to_types(grpc_repository_index_request):
    repository_index_request = RepositoryIndexRequestConverter.to_types(
        grpc_repository_index_request
    )

    assert repository_index_request.ready == grpc_repository_index_request.ready


def test_repositoryindexresponse_from_types(repository_index_response):
    grpc_repository_index_request = RepositoryIndexResponseConverter.from_types(
        repository_index_response
    )

    assert len(grpc_repository_index_request.models) == len(repository_index_response)

    for expected, grpc_model in zip(
        repository_index_response, grpc_repository_index_request.models
    ):
        assert expected.name == grpc_model.name
        assert expected.version == grpc_model.version
        assert expected.state.value == grpc_model.state
        assert expected.reason == grpc_model.reason


def test_parameters_to_types(grpc_parameters):
    parameters = ParametersConverter.to_types(grpc_parameters)

    assert parameters.content_type == grpc_parameters["content_type"].string_param
    assert parameters.foo == grpc_parameters["foo"].bool_param
    assert parameters.bar == grpc_parameters["bar"].int64_param


def test_parameters_from_types(grpc_parameters):
    parameters = ParametersConverter.to_types(grpc_parameters)
    conv_parameters = ParametersConverter.from_types(parameters)

    assert conv_parameters == grpc_parameters
