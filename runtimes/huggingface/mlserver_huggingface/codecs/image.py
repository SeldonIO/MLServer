import io
import base64
from typing import List, Any, Union
from PIL import Image
from mlserver.codecs.base import InputCodec, register_input_codec
from mlserver.codecs.lists import as_list, is_list_of
from mlserver.types import RequestInput, ResponseOutput, Parameters
from functools import partial


def _pil_base64encode(img: "Image.Image", use_bytes: bool = False) -> Union[bytes, str]:
    buf = io.BytesIO()
    img.save(buf, format=img.format)
    if use_bytes:
        return base64.b64encode(buf.getvalue())
    return base64.b64encode(buf.getvalue()).decode()


def _pil_base64decode(imgbytes: Union[bytes, str]) -> "Image.Image":
    if isinstance(imgbytes, bytes):
        imgbytes = imgbytes.decode()
    buf = io.BytesIO(base64.b64decode(imgbytes))
    return Image.open(buf)


@register_input_codec
class PILImageCodec(InputCodec):
    """
    Codec that convers to / from a PIL.Image input.
    """

    ContentType = "pillow_image"
    TypeHint = List[bytes]

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, Image.Image)

    @classmethod
    def encode_output(
        cls, name: str, payload: List[Image.Image], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:
        packed = map(partial(_pil_base64encode, use_bytes=use_bytes), payload)
        shape = [len(payload), 1]
        return ResponseOutput(
            name=name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[bytes]:
        packed = response_output.data.__root__
        return list(map(_pil_base64decode, as_list(packed)))

    @classmethod
    def encode_input(
        cls, name: str, payload: List[bytes], use_bytes: bool = True, **kwargs
    ) -> RequestInput:
        output = cls.encode_output(name, payload, use_bytes)
        return RequestInput(
            name=output.name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[bytes]:
        packed = request_input.data.__root__
        return list(map(_pil_base64decode, as_list(packed)))
