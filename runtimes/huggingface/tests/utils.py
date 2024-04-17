import os
import io
import base64
from typing import Union
from PIL import Image
from mlserver_huggingface.codecs.image import _pil_base64encode, _pil_base64decode

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


def file_path(fname: str) -> str:
    return os.path.join(TESTDATA_PATH, fname)


def file_content(fname: str) -> str:
    with open(file_path(fname), "r") as f:
        return f.read()


def file_bytescontent(fname: str) -> bytes:
    with open(file_path(fname), "rb") as f:
        return f.read()


def open_image(fname: str) -> "Image.Image":
    return Image.open(file_path(fname))


def image_base64(fname: str, use_bytes: bool = False) -> Union[str, bytes]:
    return _pil_base64encode(open_image(file_path(fname)), use_bytes=use_bytes)


def image_base64_bytes(fname: str) -> bytes:
    """Load an image by filename and return it as Base64 encoded bytes"""
    img = Image.open(
        file_path(fname),
        formats=None,  # Try and support all formats
    )

    fmt = img.format
    if fmt is None:
        raise ValueError("test image has no specified format")

    buf = io.BytesIO()
    img.save(buf, format=fmt)
    v = base64.b64encode(buf.getvalue())

    bytes = f"data:image/{fmt.lower()};base64,".encode() + v

    return bytes


def image_base64_str(fname: str) -> str:
    return image_base64_bytes(fname).decode()


# why not "Image.open", Pillow save would change image quality,
#  which caused file content changed
def build_image(fname: str) -> "Image.Image":
    return _pil_base64decode(image_base64(fname))
