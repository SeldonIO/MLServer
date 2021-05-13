from typing import Any, Dict

from .types import RequestInput, ResponseOutput, TensorData


class Codec:
    """
    The Codec interface lets you define type conversions of your raw data to /
    from the V2 Inference Protocol level.
    """

    def encode(self, payload: Any, response_output: ResponseOutput) -> ResponseOutput:
        raise NotImplementedError()

    def decode(self, request_input: RequestInput) -> Any:
        raise NotImplementedError()


class _CodecRegistry:
    """
    CodecRegistry is a "fancy" dictionary to register and find codecs.
    This class has a singleton instance exposed at the module leve, which
    should be used preferably.
    """

    def __init__(self, codecs: Dict[str, Codec] = {}):
        self._codecs = codecs

    def register(self, name: str, codec: Codec):
        # TODO: Raise error if codec exists?
        self._codecs[name] = codec

    def find_codec(self, name: str) -> Codec:
        # TODO: Raise error if codec doesn't exist
        return self._codecs[name]


class StringCodec(Codec):
    """
    Encodes a Python string as a BYTES input.
    """

    _str_codec = "utf-8"

    def encode(self, payload: str, response_output: ResponseOutput) -> ResponseOutput:
        encoded = payload.encode(self._str_codec)

        response_output.data = TensorData.parse_obj(encoded)
        response_output.datatype = "BYTES"
        response_output.shape = [len(encoded)]

        return response_output

    def decode(self, request_input: RequestInput) -> str:
        encoded = request_input.data.__root__

        if isinstance(encoded, bytes):
            return encoded.decode(self._str_codec)

        if isinstance(encoded, str):
            # NOTE: It may be a string already when decoded from json
            return encoded

        # TODO: Should we raise an error here?
        return ""


_codec_registry = _CodecRegistry({"str": StringCodec()})
