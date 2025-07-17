from typing import List, Any
from mlserver.codecs.base import InputCodec, register_input_codec
from mlserver.types import RequestInput, ResponseOutput, Parameters
from transformers.pipelines import Conversation
from mlserver.codecs.lists import is_list_of
from .utils import json_decode, json_encode, get_conversation_class


Conversation = get_conversation_class()


@register_input_codec
class HuggingfaceConversationCodec(InputCodec):
    """
    Codec that convers to / from a transformers Conversation input.
    """

    ContentType = "hg_conversation"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return Conversation is not None and is_list_of(payload, Conversation)

    @classmethod
    def encode_output(
        cls, name: str, payload: List[Any], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:
        if Conversation is None:
            raise ImportError("transformers.pipelines.Conversation is not available.")
        encoded = [json_encode(item, use_bytes=use_bytes) for item in payload]
        shape = [len(encoded), 1]
        return ResponseOutput(
            name=name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype="BYTES",
            shape=shape,
            data=encoded,
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[Any]:
        packed = response_output.data
        return [json_decode(item) for item in packed]

    @classmethod
    def encode_input(
        cls, name: str, payload: List[Any], use_bytes: bool = True, **kwargs
    ) -> RequestInput:
        if Conversation is None:
            raise ImportError("transformers.pipelines.Conversation is not available.")
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
    def decode_input(cls, request_input: RequestInput) -> List[Any]:
        packed = request_input.data
        return [json_decode(item) for item in packed]
