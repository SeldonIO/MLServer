import pytest
import uuid
from mlserver.types import RequestInput, ResponseOutput, Parameters, TensorData
from transformers.pipelines import Conversation
from mlserver_huggingface.codecs import HuggingfaceConversationCodec


@pytest.mark.parametrize(
    "name, var, use_bytes, expected1, expected2",
    [
        (
            "conversation",
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
            False,
            True,
            RequestInput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=TensorData(
                    root=[
                        '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                        '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                    ]
                ),
            ),
        ),
        (
            "conversation",
            [
                Conversation(
                    text="hello",
                    conversation_id=uuid.UUID("8524ebb5-2f63-4f36-866f-f6152e9da03f"),
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
            True,
            True,
            RequestInput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=TensorData(
                    root=[
                        b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                        b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                    ]
                ),
            ),
        ),
        (
            "conversation",
            Conversation(
                text="hello",
                conversation_id=uuid.UUID("8524ebb5-2f63-4f36-866f-f6152e9da03f"),
            ),
            True,
            False,
            None,
        ),
    ],
)
def test_encode_input(name, var, use_bytes, expected1, expected2):
    can_encode = HuggingfaceConversationCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert (
            HuggingfaceConversationCodec.encode_input(name, var, use_bytes=use_bytes)
            == expected2
        )


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            RequestInput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=TensorData(
                    root=[
                        '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                        '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                    ]
                ),
            ),
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
        ),
        (
            RequestInput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=TensorData(
                    root=[
                        b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                        b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                    ]
                ),
            ),
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
        ),
    ],
)
def test_decode_input(var, expected):
    assert HuggingfaceConversationCodec.decode_input(var) == expected


@pytest.mark.parametrize(
    "name, var, use_bytes, expected1, expected2",
    [
        (
            "conversation",
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
            False,
            True,
            ResponseOutput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=TensorData(
                    root=[
                        '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                        '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                    ]
                ),
            ),
        ),
        (
            "conversation",
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
            True,
            True,
            ResponseOutput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=TensorData(
                    root=[
                        b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                        b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                    ]
                ),
            ),
        ),
        (
            "conversation",
            Conversation(
                text="hello",
                conversation_id=uuid.UUID("8524ebb5-2f63-4f36-866f-f6152e9da03f"),
            ),
            True,
            False,
            None,
        ),
    ],
)
def test_encode_output(name, var, use_bytes, expected1, expected2):
    can_encode = HuggingfaceConversationCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert (
            HuggingfaceConversationCodec.encode_output(name, var, use_bytes=use_bytes)
            == expected2
        )


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            ResponseOutput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=[
                    '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                    '{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                ],
            ),
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
        ),
        (
            ResponseOutput(
                name="conversation",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceConversationCodec.ContentType
                ),
                data=[
                    b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                    b'{"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "how\'s it going"}',  # noqa
                ],
            ),
            [
                Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
                Conversation(
                    text="how's it going",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            ],
        ),
    ],
)
def test_decode_output(var, expected):
    assert HuggingfaceConversationCodec.decode_output(var) == expected
