from ..types import RequestInput, ResponseOutput

from .base import InputCodec, register_input_codec

ContentType = "str"


@register_input_codec(ContentType)
class StringCodec(InputCodec):
    """
    Encodes a Python string as a BYTES input.
    """

    _str_codec = "utf-8"

    def encode(self, name: str, payload: str) -> ResponseOutput:
        encoded = payload.encode(self._str_codec)

        return ResponseOutput(
            name=name, datatype="BYTES", shape=[len(encoded)], data=encoded
        )

    def decode(self, request_input: RequestInput) -> str:
        encoded = request_input.data.__root__

        if isinstance(encoded, bytes):
            return encoded.decode(self._str_codec)

        if isinstance(encoded, str):
            # NOTE: It may be a string already when decoded from json
            return encoded

        # TODO: Should we raise an error here?
        return ""
