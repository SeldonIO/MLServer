import json

from pytest_cases import fixture, parametrize_with_cases
from transformers.pipelines.question_answering import QuestionAnsweringPipeline

from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest
from mlserver_huggingface import HuggingFaceRuntime


@fixture
@parametrize_with_cases("model_settings")
async def future_runtime(model_settings: ModelSettings) -> HuggingFaceRuntime:
    # NOTE: The pytest-cases doesn't work too well yet with AsyncIO, therefore
    # we need to treat the fixture as an Awaitable and await it in the tests.
    # https://github.com/smarie/python-pytest-cases/issues/286
    runtime = HuggingFaceRuntime(model_settings)
    runtime.ready = await runtime.load()
    return runtime


async def test_load(future_runtime: HuggingFaceRuntime):
    runtime = future_runtime
    assert runtime.ready
    assert isinstance(runtime._model, QuestionAnsweringPipeline)


async def test_unload(future_runtime: HuggingFaceRuntime):
    runtime = future_runtime
    assert runtime.ready

    unloaded = await runtime.unload()
    assert unloaded


async def test_infer(
    future_runtime: HuggingFaceRuntime, inference_request: InferenceRequest
):
    runtime = future_runtime
    res = await runtime.predict(inference_request)
    pred = json.loads(res.outputs[0].data[0])
    assert pred["answer"] == "Seldon"


async def test_infer_multiple(
    future_runtime: HuggingFaceRuntime, inference_request: InferenceRequest
):
    runtime = future_runtime

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
