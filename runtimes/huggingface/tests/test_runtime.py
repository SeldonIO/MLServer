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
