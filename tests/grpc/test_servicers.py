from mlserver.grpc import dataplane_pb2 as pb
from mlserver import __version__


def test_server_live(inference_service_stub):
    req = pb.ServerLiveRequest()
    response = inference_service_stub.ServerLive(req)

    assert response.live


def test_server_ready(inference_service_stub):
    req = pb.ServerReadyRequest()
    response = inference_service_stub.ServerReady(req)

    assert response.ready


def test_model_ready(inference_service_stub, sum_model):
    req = pb.ModelReadyRequest(name=sum_model.name, version=sum_model.version)
    response = inference_service_stub.ModelReady(req)

    assert response.ready


def test_server_metadata(inference_service_stub):
    req = pb.ServerMetadataRequest()
    response = inference_service_stub.ServerMetadata(req)

    assert response.name == "mlserver"
    assert response.version == __version__
    assert response.extensions == []


def test_model_metadata(inference_service_stub, sum_model_settings):
    req = pb.ModelMetadataRequest(
        name=sum_model_settings.name, version=sum_model_settings.version
    )
    response = inference_service_stub.ModelMetadata(req)

    assert response.name == sum_model_settings.name
    assert response.platform == sum_model_settings.platform
    assert response.versions == sum_model_settings.versions


def test_model_infer(inference_service_stub, model_infer_request):
    prediction = inference_service_stub.ModelInfer(model_infer_request)

    expected = pb.InferTensorContents(fp32_contents=[21.0])

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].contents == expected
