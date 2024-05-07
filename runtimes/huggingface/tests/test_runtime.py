from pytest_cases import fixture, parametrize_with_cases

from typing import Tuple

from transformers.pipelines.text_generation import TextGenerationPipeline
from transformers.pipelines.question_answering import QuestionAnsweringPipeline
from transformers.pipelines import Pipeline

from mlserver.settings import ModelSettings
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    TensorData,
    ResponseOutput,
    Parameters,
)
from mlserver_huggingface import HuggingFaceRuntime

test_inputs_outputs = Tuple[
    HuggingFaceRuntime,
    InferenceRequest,
    InferenceResponse,
    Pipeline,
]


# This whole paramaterisation is a slight misuse. Ideally the
# different fixtures being created wouldn't all be done in this
# function, and wouldn't be returned as 1 big tuple, that needs to be
# expanded.
@fixture
@parametrize_with_cases("model_settings")
async def future_runtime(
    model_settings: ModelSettings,
) -> test_inputs_outputs:
    # NOTE: The pytest-cases doesn't work too well yet with AsyncIO, therefore
    # we need to treat the fixture as an Awaitable and await it in the tests.
    # https://github.com/smarie/python-pytest-cases/issues/286
    runtime = HuggingFaceRuntime(model_settings)
    runtime.ready = await runtime.load()

    if runtime.hf_settings.task == "question-answering":
        inference_request = InferenceRequest(
            inputs=[
                RequestInput(
                    name="question",
                    shape=[1],
                    datatype="BYTES",
                    data=["what is your name?"],
                ),
                RequestInput(
                    name="context",
                    shape=[1],
                    datatype="BYTES",
                    data=["Hello, I am Seldon, how is it going"],
                ),
            ]
        )

        inference_response = InferenceResponse(
            model_name="foo",
            model_version=None,
            id=None,
            parameters=None,
            outputs=[
                ResponseOutput(
                    name="output",
                    shape=[1, 1],
                    datatype="BYTES",
                    parameters=Parameters(content_type="hg_jsonlist", headers=None),
                    data=TensorData(
                        root=[
                            b'{"score": 0.9869917035102844, "start": 12, "end": 18, "answer": "Seldon"}'  # noqa: E501
                        ]
                    ),
                )
            ],
        )

        pipeline_kind = QuestionAnsweringPipeline
    elif runtime.hf_settings.task == "text-generation":
        inference_request = InferenceRequest(
            inputs=[
                RequestInput(
                    name="text_inputs",
                    shape=[1],
                    datatype="BYTES",
                    data=["The capital of France is called"],
                ),
            ]
        )

        inference_response = InferenceResponse(
            model_name="foo",
            model_version=None,
            id=None,
            parameters=None,
            outputs=[
                ResponseOutput(
                    name="output",
                    shape=[1, 1],
                    datatype="BYTES",
                    parameters=Parameters(content_type="hg_jsonlist", headers=None),
                    data=TensorData(
                        root=[
                            b'[{"generated_text": "The capital of France is called Vichy, which it\'s named after a Roman Catholic town.\\n\\n\\n\\n\\nMore than 50,000 Roman Catholic students attended the university this year.\\nLATEST STORIES\\nWife and child"}]'  # noqa: E501
                        ]
                    ),
                )
            ],
        )

        pipeline_kind = TextGenerationPipeline

    return (
        runtime,
        inference_request,
        inference_response,
        pipeline_kind,
    )


async def test_load(future_runtime: test_inputs_outputs):
    (
        runtime,
        _inference_request,
        _inference_response,
        pipeline_kind,
    ) = future_runtime

    assert runtime.ready

    assert isinstance(runtime._model, pipeline_kind)


async def test_unload(future_runtime: test_inputs_outputs):
    (
        runtime,
        _inference_request,
        _inference_response,
        _pipeline_kind,
    ) = future_runtime

    assert runtime.ready

    unloaded = await runtime.unload()
    assert unloaded


async def test_infer(future_runtime: test_inputs_outputs):
    (
        runtime,
        inference_request,
        inference_response,
        pipeline_kind,
    ) = future_runtime

    res = await runtime.predict(inference_request)

    # Since text generation with the chosen model is painfully
    # non-deterministic, we don't try and test for the output
    # matching.
    #
    # Instead, set them to dummy values. We'll still assert on the rest of the response.
    if pipeline_kind == TextGenerationPipeline:
        res.outputs[0].data = TensorData([])
        inference_response.outputs[0].data = TensorData([])

    assert res == inference_response
