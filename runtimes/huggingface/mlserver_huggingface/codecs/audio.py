import base64
from typing import List, Any, Union
from mlserver.codecs.base import InputCodec, register_input_codec
from mlserver.codecs.lists import as_list, is_list_of
from mlserver.types import RequestInput, ResponseOutput, Parameters


def _audio_base64encode(audio_bytes: bytes) -> str:
    """Encode audio bytes to base64 string"""
    return base64.b64encode(audio_bytes).decode()


def _audio_base64decode(audio_b64: Union[bytes, str]) -> bytes:
    """Decode base64 string to audio bytes"""
    if isinstance(audio_b64, bytes):
        audio_b64 = audio_b64.decode()
    return base64.b64decode(audio_b64)


@register_input_codec
class AudioBytesCodec(InputCodec):
    """
    Codec that converts to / from raw audio bytes input.
    This codec handles raw audio bytes that can be passed directly 
    to HuggingFace pipelines for automatic speech recognition.
    """

    ContentType = "audio_bytes"
    TypeHint = List[bytes]

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, bytes)

    @classmethod
    def encode_output(
        cls, name: str, payload: List[bytes], **kwargs
    ) -> ResponseOutput:
        packed = [_audio_base64encode(audio) for audio in payload]
        shape = [len(payload), 1]
        return ResponseOutput(
            name=name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype="BYTES",
            shape=shape,
            data=packed,
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[bytes]:
        packed = response_output.data.root
        return [_audio_base64decode(audio) for audio in as_list(packed)]

    @classmethod
    def encode_input(
        cls, name: str, payload: List[bytes], **kwargs
    ) -> RequestInput:
        output = cls.encode_output(name, payload)
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
        packed = request_input.data.root
        return [_audio_base64decode(audio) for audio in as_list(packed)]
