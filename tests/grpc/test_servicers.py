import pytest
import grpc

from mlserver.grpc import dataplane_pb2 as pb
from mlserver import __version__


async def test_server_live(inference_service_stub):
    req = pb.ServerLiveRequest()
    response = await inference_service_stub.ServerLive(req)

    assert response.live


async def test_server_ready(inference_service_stub):
    req = pb.ServerReadyRequest()
    response = await inference_service_stub.ServerReady(req)

    assert response.ready


async def test_model_ready(inference_service_stub, sum_model):
    req = pb.ModelReadyRequest(name=sum_model.name, version=sum_model.version)
    response = await inference_service_stub.ModelReady(req)

    assert response.ready


async def test_server_metadata(inference_service_stub):
    req = pb.ServerMetadataRequest()
    response = await inference_service_stub.ServerMetadata(req)

    assert response.name == "mlserver"
    assert response.version == __version__
    assert response.extensions == []


async def test_model_metadata(inference_service_stub, sum_model_settings):
    req = pb.ModelMetadataRequest(
        name=sum_model_settings.name, version=sum_model_settings.version
    )
    response = await inference_service_stub.ModelMetadata(req)

    assert response.name == sum_model_settings.name
    assert response.platform == sum_model_settings.platform
    assert response.versions == sum_model_settings.versions


@pytest.mark.parametrize(
    "model_name,model_version", [("sum-model", "v1.2.3"), ("sum-model", None)]
)
async def test_model_infer(
    inference_service_stub, model_infer_request, model_name, model_version
):
    model_infer_request.model_name = model_name
    if model_version is not None:
        model_infer_request.model_version = model_version
    else:
        model_infer_request.ClearField("model_version")

    prediction = await inference_service_stub.ModelInfer(model_infer_request)

    expected = pb.InferTensorContents(fp32_contents=[21.0])

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].contents == expected


async def test_model_infer_error(inference_service_stub, model_infer_request):
    with pytest.raises(grpc.RpcError) as err:
        model_infer_request.model_name = "my-model"
        await inference_service_stub.ModelInfer(model_infer_request)

        assert err.status == grpc.Status.INVALID_ARGUMENT
        assert err.details == "Model my-model with version v1.2.3 not found"
