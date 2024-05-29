import pytest
from mlserver.types import (
    RequestInput,
    ResponseOutput,
    Parameters,
)
from mlserver_huggingface.codecs import PILImageCodec
from mlserver_huggingface.codecs.utils import EqualUtil
from ..utils import image_base64, open_image, build_image


@pytest.mark.parametrize(
    "name, var, use_bytes, expected1, expected2",
    [
        (
            "images",
            [open_image("dogs.jpg"), open_image("hancat.jpeg")],
            True,
            True,
            RequestInput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=True),
                    image_base64("hancat.jpeg", use_bytes=True),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
        ),
        (
            "images",
            [open_image("dogs.jpg"), open_image("hancat.jpeg")],
            False,
            True,
            RequestInput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=False),
                    image_base64("hancat.jpeg", use_bytes=False),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
        ),
        ("images", open_image("dogs.jpg"), False, False, None),
    ],
)
def test_encode_input(name, var, use_bytes, expected1, expected2):
    can_encode = PILImageCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert PILImageCodec.encode_input(name, var, use_bytes) == expected2


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            RequestInput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=True),
                    image_base64("hancat.jpeg", use_bytes=True),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
            [build_image("dogs.jpg"), build_image("hancat.jpeg")],
        ),
        (
            RequestInput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=False),
                    image_base64("hancat.jpeg", use_bytes=False),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
            [build_image("dogs.jpg"), build_image("hancat.jpeg")],
        ),
    ],
)
def test_decode_input(var, expected):
    assert EqualUtil.list_equal(PILImageCodec.decode_input(var), expected)


@pytest.mark.parametrize(
    "name, var, use_bytes, expected1, expected2",
    [
        (
            "images",
            [open_image("dogs.jpg"), open_image("hancat.jpeg")],
            True,
            True,
            ResponseOutput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=True),
                    image_base64("hancat.jpeg", use_bytes=True),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
        ),
        (
            "images",
            [open_image("dogs.jpg"), open_image("hancat.jpeg")],
            False,
            True,
            ResponseOutput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=False),
                    image_base64("hancat.jpeg", use_bytes=False),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
        ),
        ("images", open_image("dogs.jpg"), False, False, None),
    ],
)
def test_encode_output(name, var, use_bytes, expected1, expected2):
    can_encode = PILImageCodec.can_encode(var)
    assert can_encode == expected1
    if can_encode:
        assert PILImageCodec.encode_output(name, var, use_bytes) == expected2


@pytest.mark.parametrize(
    "var, expected",
    [
        (
            ResponseOutput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=True),
                    image_base64("hancat.jpeg", use_bytes=True),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
            [build_image("dogs.jpg"), build_image("hancat.jpeg")],
        ),
        (
            ResponseOutput(
                name="images",
                datatype="BYTES",
                data=[
                    image_base64("dogs.jpg", use_bytes=False),
                    image_base64("hancat.jpeg", use_bytes=False),
                ],
                shape=[2, 1],
                parameters=Parameters(content_type=PILImageCodec.ContentType),
            ),
            [build_image("dogs.jpg"), build_image("hancat.jpeg")],
        ),
    ],
)
def test_decode_output(var, expected):
    assert EqualUtil.list_equal(PILImageCodec.decode_output(var), expected)
