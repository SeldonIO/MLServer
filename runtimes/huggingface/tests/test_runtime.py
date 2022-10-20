import json

from transformers.pipelines.question_answering import QuestionAnsweringPipeline

from mlserver.types import InferenceRequest

from mlserver_huggingface import HuggingFaceRuntime


def test_load(runtime: HuggingFaceRuntime):
    assert runtime.ready
    assert isinstance(runtime._model, QuestionAnsweringPipeline)


async def test_infer(runtime: HuggingFaceRuntime, inference_request: InferenceRequest):
    res = await runtime.predict(inference_request)
    pred = json.loads(res.outputs[0].data[0])
    assert pred["answer"] == "Seldon"


async def test_infer_multiple(
    runtime: HuggingFaceRuntime, inference_request: InferenceRequest
):
    # Send request with two elements
    for request_input in inference_request.inputs:
        input_data = request_input.data[0]
        request_input.data.__root__ = [input_data, input_data]
        request_input.shape = [2]

    res = await runtime.predict(inference_request)

    assert len(res.outputs) == 1

    response_output = res.outputs[0]
    assert len(response_output.data) == 2
    for d in response_output.data:
        pred = json.loads(d)
        assert pred["answer"] == "Seldon"
