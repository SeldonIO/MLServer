# mypy: disable-error-code="arg-type"

import pytest
from PIL import Image
import numpy as np

from mlserver.types import (
    RequestInput,
    InferenceRequest,
    Parameters,
)
from mlserver_huggingface.codecs import HuggingfaceRequestCodec
from mlserver_huggingface.codecs.utils import EqualUtil
from transformers.pipelines import Conversation
from ..utils import (
    file_path,
    image_base64,
    image_base64_str,
    image_base64_bytes,
    build_image,
)


@pytest.mark.parametrize(
    "inputs, use_bytes, expected",
    [
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=["var1"],
                        shape=[1, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                ],
            ),
        ),
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            True,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=[b"bar1", b"bar2"],
                        shape=[2, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=[b"var1"],
                        shape=[1, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                ],
            ),
        ),
        (
            {
                "images": [
                    Image.open(file_path("dogs.jpg")),
                    Image.open(file_path("hancat.jpeg")),
                ]
            },
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="images",
                        datatype="BYTES",
                        data=[image_base64("dogs.jpg"), image_base64("hancat.jpeg")],
                        shape=[2, 1],
                        parameters=Parameters(content_type="pillow_image"),
                    ),
                ],
            ),
        ),
        (
            {
                "images": [
                    Image.open(file_path("dogs.jpg")),
                    Image.open(file_path("hancat.jpeg")),
                ]
            },
            True,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="images",
                        datatype="BYTES",
                        data=[
                            image_base64("dogs.jpg", use_bytes=True),
                            image_base64("hancat.jpeg", use_bytes=True),
                        ],
                        shape=[2, 1],
                        parameters=Parameters(content_type="pillow_image"),
                    ),
                ],
            ),
        ),
        (
            {
                "conversations": [
                    Conversation(
                        text="hello",
                        conversation_id="0576f04b-9214-4210-8195-7ac88c741d72",
                    ),
                    Conversation(
                        text="bye",
                        conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                    ),
                ],
            },
            True,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="conversations",
                        datatype="BYTES",
                        data=[
                            b'{"uuid": "0576f04b-9214-4210-8195-7ac88c741d72", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                            b'{"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "bye"}',  # noqa
                        ],
                        shape=[2, 1],
                        parameters=Parameters(content_type="hg_conversation"),
                    ),
                ],
            ),
        ),
        (
            {
                "conversations": [
                    Conversation(
                        text="hello",
                        conversation_id="0576f04b-9214-4210-8195-7ac88c741d72",
                    ),
                    Conversation(
                        text="bye",
                        conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                    ),
                ],
            },
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="conversations",
                        datatype="BYTES",
                        data=[
                            '{"uuid": "0576f04b-9214-4210-8195-7ac88c741d72", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                            '{"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "bye"}',  # noqa
                        ],
                        shape=[2, 1],
                        parameters=Parameters(content_type="hg_conversation"),
                    ),
                ],
            ),
        ),
        (
            {
                "singlejson": {
                    "image": Image.open(file_path("dogs.jpg")),
                    "question": "how many dogs?",
                }
            },
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="singlejson",
                        datatype="BYTES",
                        data=[
                            '{"image": "'
                            + image_base64_str("dogs.jpg")
                            + '", "question": "how many dogs?"}'
                        ],
                        shape=[1],
                        parameters=Parameters(content_type="hg_json"),
                    ),
                ],
            ),
        ),
        (
            {
                "singlejson": {
                    "image": Image.open(file_path("dogs.jpg")),
                    "question": "how many dogs?",
                }
            },
            True,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="singlejson",
                        datatype="BYTES",
                        data=[
                            b'{"image": "'
                            + image_base64_bytes("dogs.jpg")
                            + b'", "question": "how many dogs?"}'
                        ],
                        shape=[1],
                        parameters=Parameters(content_type="hg_json"),
                    ),
                ],
            ),
        ),
        (
            {
                "jsonlist": [
                    {"np": np.int8([[2, 2], [2, 2]])},
                    {
                        "image": Image.open(file_path("dogs.jpg")),
                        "question": "how many dogs?",
                    },
                    {
                        "conversation": Conversation(
                            text="hi",
                            conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                        ),
                    },
                ]
            },
            True,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="jsonlist",
                        datatype="BYTES",
                        data=[
                            b'{"np": [[2, 2], [2, 2]]}',
                            b'{"image": "'
                            + image_base64_bytes("dogs.jpg")
                            + b'", "question": "how many dogs?"}',
                            b'{"conversation": {"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hi"}}',  # noqa
                        ],
                        shape=[3, 1],
                        parameters=Parameters(content_type="hg_jsonlist"),
                    ),
                ],
            ),
        ),
        (
            {
                "jsonlist": [
                    {"np": np.int8([[2, 2], [2, 2]])},
                    {
                        "image": Image.open(file_path("dogs.jpg")),
                        "question": "how many dogs?",
                    },
                    {
                        "conversation": Conversation(
                            text="hi",
                            conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                        ),
                    },
                ]
            },
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="jsonlist",
                        datatype="BYTES",
                        data=[
                            '{"np": [[2, 2], [2, 2]]}',
                            '{"image": "'
                            + image_base64_str("dogs.jpg")
                            + '", "question": "how many dogs?"}',
                            '{"conversation": {"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hi"}}',  # noqa
                        ],
                        shape=[3, 1],
                        parameters=Parameters(content_type="hg_jsonlist"),
                    ),
                ],
            ),
        ),
        (
            {"nplist": [np.int8([[2, 2], [2, 2]]), np.float64([[2, 2], [2, 2]])]},
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="nplist",
                        datatype="FP64",
                        shape=[2, 2, 2],
                        data=[2, 2, 2, 2, 2.0, 2.0, 2.0, 2.0],
                        parameters=Parameters(content_type="nplist"),
                    ),
                ],
            ),
        ),
        (
            {
                "raw_int": 1,
                "raw_float": 1.0,
                "raw_str": "foo",
            },
            False,
            InferenceRequest(
                parameters=Parameters(content_type="hf"),
                inputs=[
                    RequestInput(
                        name="raw_int",
                        datatype="BYTES",
                        shape=[1],
                        data=[1],
                        parameters=Parameters(content_type="raw"),
                    ),
                    RequestInput(
                        name="raw_float",
                        datatype="BYTES",
                        shape=[1],
                        data=[1.0],
                        parameters=Parameters(content_type="raw"),
                    ),
                    RequestInput(
                        name="raw_str",
                        datatype="BYTES",
                        shape=[1],
                        data=["foo"],
                        parameters=Parameters(content_type="raw"),
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_request(inputs, use_bytes, expected):
    payload = HuggingfaceRequestCodec.encode_request(inputs, use_bytes=use_bytes)
    # print(payload.inputs[0].data[0])
    # print(expected.inputs[0].data[0])
    assert payload == expected


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=["var1"],
                        shape=[1, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                ],
            ),
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=[b"bar1", b"bar2"],
                        shape=[2, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=[b"var1"],
                        shape=[1, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                ],
            ),
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="images",
                        datatype="BYTES",
                        data=[image_base64("dogs.jpg"), image_base64("hancat.jpeg")],
                        shape=[2, 1],
                        parameters=Parameters(content_type="pillow_image"),
                    ),
                ],
            ),
            {"images": [build_image("dogs.jpg"), build_image("hancat.jpeg")]},
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="images",
                        datatype="BYTES",
                        data=[
                            image_base64("dogs.jpg", use_bytes=True),
                            image_base64("hancat.jpeg", use_bytes=True),
                        ],
                        shape=[2, 1],
                        parameters=Parameters(content_type="pillow_image"),
                    ),
                ],
            ),
            {"images": [build_image("dogs.jpg"), build_image("hancat.jpeg")]},
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="conversations",
                        datatype="BYTES",
                        data=[
                            b'{"uuid": "0576f04b-9214-4210-8195-7ac88c741d72", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                            b'{"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "bye"}',  # noqa
                        ],
                        shape=[2, 1],
                        parameters=Parameters(content_type="hg_conversation"),
                    ),
                ],
            ),
            {
                "conversations": [
                    Conversation(
                        text="hello",
                        conversation_id="0576f04b-9214-4210-8195-7ac88c741d72",
                    ),
                    Conversation(
                        text="bye",
                        conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                    ),
                ],
            },
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="conversations",
                        datatype="BYTES",
                        data=[
                            '{"uuid": "0576f04b-9214-4210-8195-7ac88c741d72", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hello"}',  # noqa
                            '{"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "bye"}',  # noqa
                        ],
                        shape=[2, 1],
                        parameters=Parameters(content_type="hg_conversation"),
                    ),
                ],
            ),
            {
                "conversations": [
                    Conversation(
                        text="hello",
                        conversation_id="0576f04b-9214-4210-8195-7ac88c741d72",
                    ),
                    Conversation(
                        text="bye",
                        conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                    ),
                ],
            },
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="singlejson",
                        datatype="BYTES",
                        data=[
                            '{"image": "'
                            + image_base64_str("dogs.jpg")
                            + '", "question": "how many dogs?"}'
                        ],
                        shape=[1],
                        parameters=Parameters(content_type="hg_json"),
                    ),
                ],
            ),
            {
                "singlejson": {
                    "image": Image.open(file_path("dogs.jpg")),
                    "question": "how many dogs?",
                }
            },
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="singlejson",
                        datatype="BYTES",
                        data=[
                            b'{"image": "'
                            + image_base64_bytes("dogs.jpg")
                            + b'", "question": "how many dogs?"}'
                        ],
                        shape=[1],
                        parameters=Parameters(content_type="hg_json"),
                    ),
                ],
            ),
            {
                "singlejson": {
                    "image": Image.open(file_path("dogs.jpg")),
                    "question": "how many dogs?",
                }
            },
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="jsonlist",
                        datatype="BYTES",
                        data=[
                            b'{"np": [[2, 2], [2, 2]]}',
                            b'{"image": "'
                            + image_base64_bytes("dogs.jpg")
                            + b'", "question": "how many dogs?"}',
                            b'{"conversation": {"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hi"}}',  # noqa
                        ],
                        shape=[3, 1],
                        parameters=Parameters(content_type="hg_jsonlist"),
                    ),
                ],
            ),
            {
                "jsonlist": [
                    {"np": np.int8([[2, 2], [2, 2]])},
                    {
                        "image": Image.open(file_path("dogs.jpg")),
                        "question": "how many dogs?",
                    },
                    {
                        "conversation": Conversation(
                            text="hi",
                            conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                        ),
                    },
                ]
            },
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="jsonlist",
                        datatype="BYTES",
                        data=[
                            '{"np": [[2, 2], [2, 2]]}',
                            '{"image": "'
                            + image_base64_str("dogs.jpg")
                            + '", "question": "how many dogs?"}',
                            '{"conversation": {"uuid": "1031ec5b-fb76-4bb9-a55f-0f0f4ee04392", "past_user_inputs": [], "generated_responses": [], "new_user_input": "hi"}}',  # noqa
                        ],
                        shape=[3, 1],
                        parameters=Parameters(content_type="hg_jsonlist"),
                    ),
                ],
            ),
            {
                "jsonlist": [
                    {"np": np.int8([[2, 2], [2, 2]])},
                    {
                        "image": Image.open(file_path("dogs.jpg")),
                        "question": "how many dogs?",
                    },
                    {
                        "conversation": Conversation(
                            text="hi",
                            conversation_id="1031ec5b-fb76-4bb9-a55f-0f0f4ee04392",
                        ),
                    },
                ]
            },
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="nplist",
                        datatype="FP64",
                        shape=[2, 2, 2],
                        data=[2, 2, 2, 2, 2.0, 2.0, 2.0, 2.0],
                        parameters=Parameters(content_type="nplist"),
                    ),
                ],
            ),
            {"nplist": [np.int8([[2, 2], [2, 2]]), np.float64([[2, 2], [2, 2]])]},
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="raw_int",
                        datatype="BYTES",
                        shape=[1],
                        data=[1],
                        parameters=Parameters(content_type="raw"),
                    ),
                    RequestInput(
                        name="raw_float",
                        datatype="BYTES",
                        shape=[1],
                        data=[1.0],
                        parameters=Parameters(content_type="raw"),
                    ),
                    RequestInput(
                        name="raw_str",
                        datatype="BYTES",
                        shape=[1],
                        data=["foo"],
                        parameters=Parameters(content_type="raw"),
                    ),
                ],
            ),
            {
                "raw_int": 1,
                "raw_float": 1.0,
                "raw_str": "foo",
            },
        ),
    ],
)
def test_decode_request(inference_request, expected):
    payload = HuggingfaceRequestCodec.decode_request(inference_request)
    assert EqualUtil.dict_equal(payload, expected)


def test_encode_response():
    pass


def test_decode_response():
    pass
