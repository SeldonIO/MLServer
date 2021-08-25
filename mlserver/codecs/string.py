from typing import Generator, Union, List

from ..types import RequestInput, ResponseOutput

from .utils import FirstInputRequestCodec
from .base import InputCodec, register_input_codec, register_request_codec

_DefaultStrCodec = "utf-8"


def _decode_str(encoded: Union[str, bytes], str_codec=_DefaultStrCodec) -> str:
    if isinstance(encoded, bytes):
        return encoded.decode(str_codec)

    if isinstance(encoded, str):
        # NOTE: It may be a string already when decoded from json
        return encoded

    # TODO: Should we raise an error here?
    return ""


def _split_elements(
    encoded: Union[bytes, str, List[str]], shape: List[int]
) -> Generator[Union[str, bytes], None, None]:
    if isinstance(encoded, list):
        # If it's a list, assume list of strings
        yield from encoded
    elif isinstance(encoded, bytes):
        if len(shape) == 0:
            # If there is no shape, assume that it's a single element
            yield encoded
        else:
            # Otherwise, assume content is a concatenated list of same-length
            # strings and get the common length from the shape
            common_length = shape[-1]
            for i in range(0, len(encoded), common_length):
                yield encoded[i : i + common_length]
    elif isinstance(encoded, str):
        yield encoded


@register_input_codec
class StringCodec(InputCodec):
    """
    Encodes a Python string as a BYTES input.
    """

    ContentType = "str"

    @classmethod
    def encode(cls, name: str, payload: List[str]) -> ResponseOutput:
        packed = b""
        common_length = None
        for elem in payload:
            as_bytes = elem.encode(_DefaultStrCodec)

            # TODO: Should we use the length of the UTF8 string or the bytes
            # array?
            elem_length = len(as_bytes)
            if common_length is None:
                common_length = elem_length

            if common_length != elem_length:
                # TODO: Raise an error here
                # TODO: Should we try to add padding?
                pass

            packed += as_bytes

        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=[len(payload), common_length],
            data=packed,
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> List[str]:
        encoded = request_input.data.__root__
        shape = request_input.shape

        return [_decode_str(elem) for elem in _split_elements(encoded, shape)]


@register_request_codec
class StringRequestCodec(FirstInputRequestCodec):
    InputCodec = StringCodec
    ContentType = StringCodec.ContentType
