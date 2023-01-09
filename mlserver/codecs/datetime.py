from typing import Any, Union, List
from datetime import datetime
from functools import partial

from ..types import RequestInput, ResponseOutput
from .lists import is_list_of, as_list, ListElement
from .base import InputCodec, register_input_codec

_Datetime = Union[str, datetime]
_DatetimeStrCodec = "ascii"


def _to_iso(elem: _Datetime) -> str:
    if isinstance(elem, str):
        # Assume date has already been encoded upstream
        return elem

    return elem.isoformat()


def _encode_datetime(elem: _Datetime, use_bytes: bool) -> Union[bytes, str]:
    iso_date = _to_iso(elem)
    if not use_bytes:
        return iso_date

    return iso_date.encode(_DatetimeStrCodec)


def _ensure_str(elem: ListElement) -> str:
    if isinstance(elem, str):
        return elem

    return elem.decode(_DatetimeStrCodec)


def _decode_datetime(elem: ListElement) -> datetime:
    iso_format = _ensure_str(elem)
    return datetime.fromisoformat(iso_format)


@register_input_codec
class DatetimeCodec(InputCodec):
    """
    Codec that convers to / from a datetime input.
    """

    ContentType = "datetime"
    TypeHint = List[_Datetime]

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, datetime)

    @classmethod
    def encode_output(
        cls, name: str, payload: List[_Datetime], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:
        packed = map(partial(_encode_datetime, use_bytes=use_bytes), payload)
        shape = [len(payload), 1]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[datetime]:
        packed = response_output.data.__root__

        return list(map(_decode_datetime, as_list(packed)))

    @classmethod
    def encode_input(
        cls, name: str, payload: List[_Datetime], use_bytes: bool = True, **kwargs
    ) -> RequestInput:
        output = cls.encode_output(name, payload, use_bytes=use_bytes)
        return RequestInput(
            name=output.name,
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[datetime]:
        packed = request_input.data.__root__

        return list(map(_decode_datetime, as_list(packed)))
