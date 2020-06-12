from mlserver.grpc import dataplane_pb2 as pb


def test_inference_service_infer(inference_service_stub, model_infer_request):
    prediction = inference_service_stub.ModelInfer(model_infer_request)

    expected = pb.InferTensorContents(fp32_contents=[21.0])

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].contents == expected
