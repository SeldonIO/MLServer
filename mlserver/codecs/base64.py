import base64
import binascii

from typing import Any, List, Union
from functools import partial

from ..types import RequestInput, ResponseOutput
from .lists import is_list_of
from .base import InputCodec, register_input_codec
from .lists import as_list, ListElement

_Base64StrCodec = "ascii"


def _ensure_bytes(elem: ListElement) -> bytes:
    if isinstance(elem, str):
        return elem.encode(_Base64StrCodec)

    return elem


def _encode_base64(elem: ListElement, use_bytes: bool) -> Union[bytes, str]:
    as_bytes = _ensure_bytes(elem)
    b64_encoded = base64.b64encode(as_bytes)
    if use_bytes:
        return b64_encoded

    return b64_encoded.decode(_Base64StrCodec)


def _decode_base64(elem: ListElement) -> bytes:
    as_bytes = _ensure_bytes(elem)

    # Check that the input is valid base64.
    # Otherwise, convert into base64.
    try:
        return base64.b64decode(as_bytes, validate=True)
    except binascii.Error:
        return as_bytes


@register_input_codec
class Base64Codec(InputCodec):
    """
    Codec that convers to / from a base64 input.
    """

    ContentType = "base64"
    TypeHint = List[bytes]

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, bytes)

    @classmethod
    def encode_output(
        cls, name: str, payload: List[bytes], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:
        # Assume that payload is already in b64, so we only need to pack it
        packed = map(partial(_encode_base64, use_bytes=use_bytes), payload)
        shape = [len(payload), 1]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[bytes]:
        packed = response_output.data.__root__
        return list(map(_decode_base64, as_list(packed)))

    @classmethod
    def encode_input(
        cls, name: str, payload: List[bytes], use_bytes: bool = True, **kwargs
    ) -> RequestInput:
        # Assume that payload is already in b64, so we only need to pack it
        output = cls.encode_output(name, payload, use_bytes)
        return RequestInput(
            name=output.name,
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[bytes]:
        packed = request_input.data.__root__

        return list(map(_decode_base64, as_list(packed)))
