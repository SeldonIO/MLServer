async def test_end_2_end(
        anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
        alibi_anchor_image_model,
        payload: InferenceRequest
):
    # in this test we are getting explanation and making sure that it the same one as returned by alibi
    # directly
    runtime_result = await anchor_image_runtime_with_remote_predict_patch.predict(payload)
    decoded_runtime_results = json.loads(convert_from_bytes(runtime_result.outputs[0], ty=str))
    alibi_result = alibi_anchor_image_model.explain(NumpyCodec.decode(payload.inputs[0]))

    assert_array_equal(np.array(decoded_runtime_results["data"]["anchor"]), alibi_result.data["anchor"])