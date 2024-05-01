import pytest
import numpy as np
from transformers.pipelines import Conversation
from mlserver.types import (
    RequestInput,
    ResponseOutput,
    Parameters,
)

from mlserver_huggingface.codecs import HuggingfaceSingleJSONCodec


@pytest.mark.parametrize(
    "name, var, use_bytes, expected1, expected2",
    [
        (
            "mixed",
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
            True,
            True,
            RequestInput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    b'{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
        ),
        (
            "mixed",
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
            False,
            True,
            RequestInput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    '{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
        ),
    ],
)
def test_encode_request(name, var, use_bytes, expected1, expected2):
    can_encode = HuggingfaceSingleJSONCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert (
            HuggingfaceSingleJSONCodec.encode_input(name, var, use_bytes=use_bytes)
            == expected2
        )


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            RequestInput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    b'{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
        ),
        (
            RequestInput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    '{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
        ),
    ],
)
def test_decode_request(var, expected):
    assert HuggingfaceSingleJSONCodec.decode_input(var) == expected


@pytest.mark.parametrize(
    "name, var, use_bytes, expected1, expected2",
    [
        (
            "mixed",
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello",
                    conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f",
                ),
            },
            True,
            True,
            ResponseOutput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    b'{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
        ),
        (
            "mixed",
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
            False,
            True,
            ResponseOutput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    '{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
        ),
    ],
)
def test_encode_response(name, var, use_bytes, expected1, expected2):
    can_encode = HuggingfaceSingleJSONCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert (
            HuggingfaceSingleJSONCodec.encode_output(name, var, use_bytes=use_bytes)
            == expected2
        )


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            ResponseOutput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    b'{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
        ),
        (
            ResponseOutput(
                name="mixed",
                shape=[1],
                datatype="BYTES",
                parameters=Parameters(
                    content_type=HuggingfaceSingleJSONCodec.ContentType
                ),
                data=[
                    '{"str": "str", "npval": 1, "conversation": {"uuid": "8524ebb5-2f63-4f36-866f-f6152e9da03f", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}}'  # noqa
                ],
            ),
            {
                "str": "str",
                "npval": np.int8(1),
                "conversation": Conversation(
                    text="hello", conversation_id="8524ebb5-2f63-4f36-866f-f6152e9da03f"
                ),
            },
        ),
    ],
)
def test_decode_response(var, expected):
    assert HuggingfaceSingleJSONCodec.decode_output(var) == expected
