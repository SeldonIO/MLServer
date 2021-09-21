from typing import Union, List
from datetime import datetime

from ..types import RequestInput, ResponseOutput
from .base import InputCodec, register_input_codec
from .pack import pack, unpack, PackElement

_Datetime = Union[str, datetime]
_DatetimeStrCodec = "ascii"


def _to_iso(elem: _Datetime) -> str:
    if isinstance(elem, str):
        # Assume date has already been encoded upstream
        return elem

    return elem.isoformat()


def _encode_datetime(elem: _Datetime) -> bytes:
    iso_date = _to_iso(elem)
    return iso_date.encode(_DatetimeStrCodec)


def _ensure_str(elem: PackElement) -> str:
    if isinstance(elem, str):
        return elem

    return elem.decode(_DatetimeStrCodec)


def _decode_datetime(elem: PackElement) -> datetime:
    iso_format = _ensure_str(elem)
    return datetime.fromisoformat(iso_format)


@register_input_codec
class DatetimeCodec(InputCodec):
    """
    Codec that convers to / from a base64 input.
    """

    ContentType = "datetime"

    @classmethod
    def encode(cls, name: str, payload: List[_Datetime]) -> ResponseOutput:
        # Assume that payload is already in b64, so we only need to pack it
        packed, shape = pack(map(_encode_datetime, payload))
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=packed,
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> List[datetime]:
        packed = request_input.data.__root__
        shape = request_input.shape

        return list(map(_decode_datetime, unpack(packed, shape)))
