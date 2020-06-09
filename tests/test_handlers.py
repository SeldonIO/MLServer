def test_dataplane_infer(data_plane, sum_model, inference_request):
    prediction = data_plane.infer(sum_model.name, inference_request)
    breakpoint()

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == [21]
