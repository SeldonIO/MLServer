from ..types import RequestInput, ResponseOutput

from .base import InputCodec
from .utils import InputOrOutput
from .pack import pack, unpack


class RawInputCodec(InputCodec):
    @classmethod
    def _unpack(cls, elem: InputOrOutput, raw: bytes) -> InputOrOutput:
        # TODO: Assert that `data` field is empty
        elem.data = unpack(elem, raw)
        return elem

    @classmethod
    def encode_input(cls, request_input: RequestInput, raw: bytes) -> RequestInput:
        return cls._unpack(request_input, raw)

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> bytes:
        # pack and return packed
        return pack(request_input)

    @classmethod
    def encode_output(
        cls, response_output: ResponseOutput, raw: bytes
    ) -> ResponseOutput:
        return cls._unpack(response_output, raw)

    @classmethod
    def decode_output(cls, request_output: ResponseOutput) -> bytes:
        # pack and return packed
        return pack(request_output)
