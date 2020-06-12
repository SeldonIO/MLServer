from mlserver.grpc import dataplane_pb2 as pb


def test_server_live(inference_service_stub):
    req = pb.ServerLiveRequest()
    response = inference_service_stub.ServerLive(req)

    assert response.live


def test_server_ready(inference_service_stub):
    req = pb.ServerReadyRequest()
    response = inference_service_stub.ServerReady(req)

    assert response.ready


def test_server_model_ready(inference_service_stub, sum_model):
    req = pb.ModelReadyRequest(name=sum_model.name)
    response = inference_service_stub.ModelReady(req)

    assert response.ready


def test_model_infer(inference_service_stub, model_infer_request):
    prediction = inference_service_stub.ModelInfer(model_infer_request)

    expected = pb.InferTensorContents(fp32_contents=[21.0])

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].contents == expected
