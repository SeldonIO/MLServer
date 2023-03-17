from unittest.mock import patch

import openai
import pandas as pd
import pytest

from mlserver import ModelSettings
from mlserver.types import InferenceRequest, RequestInput, InferenceResponse
from mlserver_llm.openai.openai_runtime import OpenAIRuntime, _df_to_messages


@pytest.fixture
def chat_result() -> dict:
    return {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-3.5-turbo-0301",
        "usage": {"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
        "choices": [
            {
                "message": {"role": "assistant", "content": "\n\nThis is a test!"},
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }


async def test_openai_chat__smoke(chat_result: dict):
    dummy_api_key = "dummy_key"
    model_id = "gpt-3.5-turbo"

    model_settings = ModelSettings(
        implementation=OpenAIRuntime,
        parameters={
            "extra": {"config": {"api_key": dummy_api_key, "model_id": model_id}}
        },
    )
    rt = OpenAIRuntime(model_settings)

    async def _mocked_chat_impl(**kwargs):
        return chat_result

    with patch("openai.ChatCompletion") as mock_chat:
        mock_chat.acreate = _mocked_chat_impl
        res = await rt.predict(
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="role", shape=[1, 1], datatype="BYTES", data=["user"]
                    ),
                    RequestInput(
                        name="content", shape=[1, 1], datatype="BYTES", data=["hello"]
                    ),
                ]
            )
        )
        assert isinstance(res, InferenceResponse)


@pytest.mark.parametrize(
    "df, expected_messages",
    [
        (
            pd.DataFrame.from_dict({"role": ["user"], "content": ["hello"]}),
            [{"role": "user", "content": "hello"}],
        ),
        (
            pd.DataFrame.from_dict(
                {"role": ["user1", "user2"], "content": ["hello1", "hello2"]}
            ),
            [
                {"role": "user1", "content": "hello1"},
                {"role": "user2", "content": "hello2"},
            ],
        ),
    ],
)
def test_convert_df_to_messages(df: pd.DataFrame, expected_messages: list[dict]):
    messages = _df_to_messages(df)
    assert messages == expected_messages


@pytest.mark.parametrize(
    "api_key, organization",
    [
        ("dummy_key", None),
        ("dummy_key", "dummy_org"),
    ],
)
async def test_api_key_and_org_set(api_key: str, organization: str):
    model_id = "gpt-3.5-turbo"

    config = {"api_key": api_key, "model_id": model_id}
    if organization:
        config["organization"] = organization

    model_settings = ModelSettings(
        implementation=OpenAIRuntime, parameters={"extra": {"config": config}}
    )
    rt = OpenAIRuntime(model_settings)

    assert rt._api_key == api_key
    assert rt._organization == organization

    # check that api_key not set globally
    assert openai.api_key is None
    assert openai.organization is None
