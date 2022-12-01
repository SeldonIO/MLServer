import pytest
from mlserver.settings import ModelSettings, ModelParameters
from mlserver_huggingface import HuggingFaceRuntime
from mlserver_huggingface.codecs import HuggingfaceRequestCodec
from ..utils import file_path, open_image


@pytest.fixture
def current_model_settings(request) -> ModelSettings:
    if not request.config.option.test_hg_tasks:
        pytest.skip()
    return ModelSettings(
        name="model",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(extra={"task": "visual-question-answering"}),
    )


@pytest.fixture
async def current_runtime(current_model_settings: ModelSettings) -> HuggingFaceRuntime:
    runtime = HuggingFaceRuntime(current_model_settings)
    await runtime.load()
    return runtime


@pytest.fixture
def visual_qa_request():
    inputs = [
        {
            "image": file_path("dogs.jpg"),
            "question": "what's that animal",
        },
        {
            "image": open_image("ugcat.jpeg"),
            "question": "what's that animal",
        },
    ]
    req = HuggingfaceRequestCodec.encode_request(
        {"array_inputs": inputs}, use_bytes=False
    )
    return req


@pytest.fixture
def visual_qa_request_with_extra_args():
    inputs = [
        {
            "image": file_path("dogs.jpg"),
            "question": "what's that animal",
        },
        {
            "image": open_image("ugcat.jpeg"),
            "question": "what's that animal",
        },
    ]
    req = HuggingfaceRequestCodec.encode_request(
        {"array_inputs": inputs, "top_k": 1}, use_bytes=False
    )
    return req


async def test_infer(current_runtime, visual_qa_request):
    resp = await current_runtime.predict(visual_qa_request)
    decoded = HuggingfaceRequestCodec.decode_response(resp)
    assert len(decoded) == 2
    assert len(decoded[0]) > 1
    assert len(decoded[1]) > 1
    assert decoded[0][0]["answer"] == "dog"
    assert decoded[1][0]["answer"] == "cat"


async def test_infer_with_extra_args(
    current_runtime, visual_qa_request_with_extra_args
):
    resp = await current_runtime.predict(visual_qa_request_with_extra_args)
    decoded = HuggingfaceRequestCodec.decode_response(resp)
    assert len(decoded) == 2
    assert len(decoded[0]) == 1
    assert len(decoded[1]) == 1
    assert decoded[0][0]["answer"] == "dog"
    assert decoded[1][0]["answer"] == "cat"
