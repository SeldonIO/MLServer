import pytest
from mlserver.settings import ModelSettings, ModelParameters
from mlserver_huggingface import HuggingFaceRuntime
from mlserver_huggingface.codecs import HuggingfaceRequestCodec


test_sentence = "実際に空が[MASK]のか？"


@pytest.fixture
def current_model_settings(request) -> ModelSettings:
    if not request.config.option.test_hg_tasks:
        pytest.skip()
    return ModelSettings(
        name="model",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(
            extra={
                "task": "fill-mask",
                "pretrained_model": "cl-tohoku/bert-base-japanese",
                "pretrained_tokenizer": "cl-tohoku/bert-base-japanese",
            }
        ),
    )


@pytest.fixture
async def current_runtime(current_model_settings: ModelSettings) -> HuggingFaceRuntime:
    runtime = HuggingFaceRuntime(current_model_settings)
    await runtime.load()
    return runtime


@pytest.fixture
def japanese_text_request():
    inputs = [test_sentence]
    req = HuggingfaceRequestCodec.encode_request(
        {"inputs": inputs},
        use_bytes=False,
    )
    return req


async def test_infer(current_runtime, japanese_text_request):
    resp = await current_runtime.predict(japanese_text_request)
    decoded = HuggingfaceRequestCodec.decode_response(resp)
    top_result = list(decoded.items())[0][1][0]
    assert top_result["token_str"] == "見える", "Inference is incorrect!"
