import pytest
import numpy as np
from PIL import Image
from mlserver.types import RequestInput, ResponseOutput, Parameters, TensorData
from transformers.pipelines import Conversation
from mlserver_huggingface.codecs import HuggingfaceListJSONCodec
from mlserver_huggingface.codecs.utils import EqualUtil
from ..utils import file_path, file_content


@pytest.mark.parametrize(
    "name, var, expected1, expected2",
    [
        (
            "list",
            [
                {
                    "str": "str",
                    "npval": np.int8(1),
                    "pil": Image.open(file_path("hancat.jpeg")),
                    "conversation": Conversation(text="hhhh"),
                },
                {
                    "nested": {
                        "str": "str",
                        "npval": np.int8(1),
                        "pil": Image.open(file_path("hancat.jpeg")),
                    }
                },
            ],
            True,
            RequestInput(
                name="list",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(__root__=[]),
            ),
        ),
        ("mixed", [1, {}], False, None),
    ],
)
def test_encode_input(name, var, expected1, expected2):
    can_encode = HuggingfaceListJSONCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        encoded = HuggingfaceListJSONCodec.encode_input(name, var)
        assert encoded.name == expected2.name
        assert encoded.shape == expected2.shape
        assert encoded.datatype == expected2.datatype
        assert encoded.parameters == expected2.parameters


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            RequestInput(
                name="list",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(__root__=["{}", "{}"]),
            ),
            [{}, {}],
        ),
        (
            RequestInput(
                name="with_image",
                shape=[1, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(__root__=[file_content("image_base64.txt")]),
            ),
            [{"i": Image.open(file_path("dogs.jpg"))}],
        ),
        (
            RequestInput(
                name="with_conversation",
                shape=[1, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(
                    __root__=[
                        '{"uuid": "59a1121c-831b-40ae-b33b-320b9dd60770", "past_user_inputs": [], "new_user_input": "hi", "generated_responses": []}'  # noqa
                    ]
                ),
            ),
            [
                Conversation(
                    conversation_id="59a1121c-831b-40ae-b33b-320b9dd60770",
                    past_user_inputs=[],
                    text="hi",
                    generated_responses=[],
                )
            ],
        ),
        (
            RequestInput(
                name="mixed",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(
                    __root__=[
                        '{"c": {"uuid": "59a1121c-831b-40ae-b33b-320b9dd60770", "past_user_inputs": [], "new_user_input": "hi", "generated_responses": []}}',  # noqa
                        file_content("image_base64.txt"),
                    ]
                ),
            ),
            [
                {
                    "c": Conversation(
                        conversation_id="59a1121c-831b-40ae-b33b-320b9dd60770",
                        past_user_inputs=[],
                        text="hi",
                        generated_responses=[],
                    )
                },
                {"i": Image.open(file_path("dogs.jpg"))},
            ],
        ),
    ],
)
def test_decode_input(var, expected):
    decoded = HuggingfaceListJSONCodec.decode_input(var)
    assert EqualUtil.list_equal(decoded, expected)


@pytest.mark.parametrize(
    "name, var, expected",
    [
        (
            "list",
            [
                {
                    "str": "str",
                    "npval": np.int8(1),
                    "pil": Image.open(file_path("hancat.jpeg")),
                    "conversation": Conversation(text="hhhh"),
                },
                {
                    "nested": {
                        "str": "str",
                        "npval": np.int8(1),
                        "pil": Image.open(file_path("hancat.jpeg")),
                    }
                },
            ],
            RequestInput(
                name="list",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(__root__=["{}", "{}"]),
            ),
        )
    ],
)
def test_encode_output(name, var, expected):
    encoded = HuggingfaceListJSONCodec.encode_output(name, var)
    assert encoded.name == expected.name
    assert encoded.shape == expected.shape
    assert encoded.datatype == expected.datatype
    assert encoded.parameters == expected.parameters


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            ResponseOutput(
                name="list",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(__root__=["{}", "{}"]),
            ),
            [{}, {}],
        ),
        (
            ResponseOutput(
                name="with_image",
                shape=[1, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(__root__=[file_content("image_base64.txt")]),
            ),
            [{"i": Image.open(file_path("dogs.jpg"))}],
        ),
        (
            ResponseOutput(
                name="with_conversation",
                shape=[1, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(
                    __root__=[
                        '{"uuid": "59a1121c-831b-40ae-b33b-320b9dd60770", "past_user_inputs": [], "new_user_input": "hi", "generated_responses": []}'  # noqa
                    ]
                ),
            ),
            [
                Conversation(
                    conversation_id="59a1121c-831b-40ae-b33b-320b9dd60770",
                    past_user_inputs=[],
                    text="hi",
                    generated_responses=[],
                )
            ],
        ),
        (
            ResponseOutput(
                name="mixed",
                shape=[2, 1],
                datatype="BYTES",
                parameters=Parameters(content_type="hg_jsonlist"),
                data=TensorData(
                    __root__=[
                        '{"c": {"uuid": "59a1121c-831b-40ae-b33b-320b9dd60770", "past_user_inputs": [], "new_user_input": "hi", "generated_responses": []}}',  # noqa
                        file_content("image_base64.txt"),
                    ]
                ),
            ),
            [
                {
                    "c": Conversation(
                        conversation_id="59a1121c-831b-40ae-b33b-320b9dd60770",
                        past_user_inputs=[],
                        text="hi",
                        generated_responses=[],
                    )
                },
                {"i": Image.open(file_path("dogs.jpg"))},
            ],
        ),
    ],
)
def test_decode_output(var, expected):
    assert EqualUtil.list_equal(HuggingfaceListJSONCodec.decode_output(var), expected)
