import pytest
from mlserver.settings import ModelSettings, ModelParameters
from mlserver_huggingface import HuggingFaceRuntime
from mlserver_huggingface.codecs import HuggingfaceRequestCodec


"""
Test case summary:

1. Short sentence with a single masked word.


Input: 実際に空が[MASK]のか？ English: Is the sky truly [MASK]?

Output: ある　ー＞ English: Does the sky truly exist?

Model: izumi-lab/bert-small-japanese (a 70 MB masked language model
trained on a mask filling task.)

"""


@pytest.mark.parametrize(
    "test_sentence,expected_output,model_parameters",
    [
        (
            "実際に空が[MASK]のか？",
            "ある",
            ModelParameters(
                extra={
                    "task": "fill-mask",
                    "pretrained_model": "izumi-lab/bert-small-japanese",
                    "pretrained_tokenizer": "izumi-lab/bert-small-japanese",
                }
            ),
        )
    ],
)
async def test_infer(test_sentence, expected_output, model_parameters, request):
    if (not request.config.option.test_hg_tasks) or (
        not request.config.option.test_ja_support
    ):
        pytest.skip()

    # Get
    reqs = HuggingfaceRequestCodec.encode_request(
        {"inputs": [test_sentence]},
        use_bytes=False,
    )

    # Load model
    bert_japanese_settings = ModelSettings(
        name="model", implementation=HuggingFaceRuntime, parameters=model_parameters
    )

    # Create runtime
    runtime = HuggingFaceRuntime(bert_japanese_settings)
    await runtime.load()

    # Generate response
    resp = await runtime.predict(reqs)
    decoded = HuggingfaceRequestCodec.decode_response(resp)

    # Get top result
    top_result = decoded["output"][0]
    assert top_result["token_str"] == expected_output, "Inference is correct!"
