import functools

from typing import Any, ClassVar, Dict, Iterable, Optional, Type, Union

from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput
from ..logging import logger

InputCodecLike = Union[Type["InputCodec"], "InputCodec"]
RequestCodecLike = Union[Type["RequestCodec"], "RequestCodec"]


def deprecated(reason: str):
    def _deprecated(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            logger.warning(f"DEPRECATED! {reason}")
            return func(*args, **kwargs)

        return _inner

    return _deprecated


class InputCodec:
    """
    The InputCodec interface lets you define type conversions of your raw input
    data to / from the Open Inference Protocol.
    Note that this codec applies at the individual input (output) level.

    For request-wide transformations (e.g. dataframes), use the
    ``RequestCodec`` interface instead.
    """

    ContentType: ClassVar[str] = ""
    TypeHint: ClassVar[Type] = type(None)

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        """
        Evaluate whether the codec can encode (decode) the payload.
        """
        return False

    @classmethod
    @deprecated("The encode() method is now deprecated. Use encode_output() instead.")
    def encode(cls, name: str, payload: Any) -> ResponseOutput:
        return cls.encode_output(name, payload)

    @classmethod
    def encode_output(cls, name: str, payload: Any, **kwargs) -> ResponseOutput:
        """
        Encode the given payload into a response output.
        """
        raise NotImplementedError()

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> Any:
        """
        Decode a response output into a high-level Python type.
        """
        raise NotImplementedError()

    @classmethod
    def encode_input(cls, name: str, payload: Any, **kwargs) -> RequestInput:
        """
        Encode the given payload into a ``RequestInput``.
        """
        raise NotImplementedError()

    @classmethod
    @deprecated("The decode() method is now deprecated. Use decode_input() instead.")
    def decode(cls, request_input: RequestInput) -> Any:
        return cls.decode_input(request_input)

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> Any:
        """
        Decode a request input into a high-level Python type.
        """
        raise NotImplementedError()


class RequestCodec:
    """
    The ``RequestCodec`` interface lets you define request-level conversions
    between high-level Python types and the Open Inference Protocol.
    This can be useful where the encoding of your payload encompases multiple
    input heads (e.g. dataframes, where each column can be thought as a
    separate input head).

    For individual input-level encoding / decoding, use the ``InputCodec``
    interface instead.
    """

    ContentType: ClassVar[str] = ""
    TypeHint: ClassVar[Type] = type(None)

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        """
        Evaluate whether the codec can encode (decode) the payload.
        """
        return False

    @classmethod
    @deprecated("The encode() method is now deprecated. Use encode_response() instead.")
    def encode(
        cls, model_name: str, payload: Any, model_version: Optional[str] = None
    ) -> InferenceResponse:
        return cls.encode_response(model_name, payload, model_version)

    @classmethod
    def encode_response(
        cls,
        model_name: str,
        payload: Any,
        model_version: Optional[str] = None,
        **kwargs,
    ) -> InferenceResponse:
        """
        Encode the given payload into an inference response.
        """
        raise NotImplementedError()

    @classmethod
    def decode_response(cls, response: InferenceResponse) -> Any:
        """
        Decode an inference response into a high-level Python object.
        """
        raise NotImplementedError()

    @classmethod
    def encode_request(cls, payload: Any, **kwargs) -> InferenceRequest:
        """
        Encode the given payload into an inference request.
        """
        raise NotImplementedError()

    @classmethod
    @deprecated("The decode() method is now deprecated. Use decode_request() instead.")
    def decode(cls, request: InferenceRequest) -> Any:
        return cls.decode_request(request)

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> Any:
        """
        Decode an inference request into a high-level Python object.
        """
        raise NotImplementedError()


def _find_codec_by_payload(
    payload: Any, codecs: Iterable[Union[RequestCodec, InputCodec]]
) -> Optional[Union[RequestCodec, InputCodec]]:
    matching_codecs = []
    for codec in codecs:
        if codec.can_encode(payload):
            matching_codecs.append(codec)

    if len(matching_codecs) == 0:
        logger.warning(f"No codec was found for payload with type {type(payload)}.")
        return None

    first_codec = matching_codecs[0]
    if len(matching_codecs) > 1:
        logger.warning(
            f"Multiple codecs ({len(matching_codecs)} were found for a "
            f"payload with type {type(payload)}. "
            f"The first one found will be used ({first_codec.ContentType})."
        )

    return first_codec


def _find_codec_by_type_hint(
    type_hint: Type, codecs: Iterable[Union[RequestCodec, InputCodec]]
) -> Optional[Union[RequestCodec, InputCodec]]:
    matching_codecs = []
    for codec in codecs:
        if codec.TypeHint == type_hint:
            matching_codecs.append(codec)

    if len(matching_codecs) == 0:
        logger.warning(f"No codec was found for type hint {type_hint}.")
        return None

    first_codec = matching_codecs[0]
    if len(matching_codecs) > 1:
        logger.warning(
            f"Multiple codecs ({len(matching_codecs)} were found for a "
            f"type hint {type_hint}. "
            f"The first one found will be used ({first_codec.ContentType})."
        )

    return first_codec


class _CodecRegistry:
    """
    CodecRegistry is a "fancy" dictionary to register and find codecs.
    This class has a singleton instance exposed at the module leve, which
    should be used preferably.
    """

    def __init__(
        self,
        input_codecs: Dict[str, InputCodecLike] = {},
        request_codecs: Dict[str, RequestCodecLike] = {},
    ):
        self._input_codecs = input_codecs
        self._request_codecs = request_codecs

    def register_input_codec(self, content_type: str, codec: InputCodecLike):
        # TODO: Raise error if codec exists?
        self._input_codecs[content_type] = codec

    def find_input_codec(
        self,
        content_type: Optional[str] = None,
        payload: Optional[Any] = None,
        type_hint: Optional[Type] = None,
    ) -> Optional[InputCodecLike]:
        if content_type:
            return self._input_codecs.get(content_type)
        elif payload:
            return self.find_input_codec_by_payload(payload)
        elif type_hint:
            return self.find_input_codec_by_type_hint(type_hint)

        return None

    def find_input_codec_by_payload(self, payload: Any) -> Optional[InputCodecLike]:
        return _find_codec_by_payload(
            payload, self._input_codecs.values()  # type: ignore
        )

    def find_input_codec_by_type_hint(
        self, type_hint: Type
    ) -> Optional[InputCodecLike]:
        return _find_codec_by_type_hint(
            type_hint, self._input_codecs.values()  # type: ignore
        )

    def register_request_codec(self, content_type: str, codec: RequestCodecLike):
        # TODO: Raise error if codec exists?
        self._request_codecs[content_type] = codec

    def find_request_codec(
        self,
        content_type: Optional[str] = None,
        payload: Optional[Any] = None,
        type_hint: Optional[Type] = None,
    ) -> Optional[RequestCodecLike]:
        if content_type:
            return self._request_codecs.get(content_type)
        elif payload:
            return self.find_request_codec_by_payload(payload)
        elif type_hint:
            return self.find_request_codec_by_type_hint(type_hint)

        return None

    def find_request_codec_by_payload(self, payload: Any) -> Optional[RequestCodecLike]:
        return _find_codec_by_payload(
            payload, self._request_codecs.values()  # type: ignore
        )

    def find_request_codec_by_type_hint(
        self, type_hint: Type
    ) -> Optional[RequestCodecLike]:
        return _find_codec_by_type_hint(
            type_hint, self._request_codecs.values()  # type: ignore
        )


_codec_registry = _CodecRegistry()

find_request_codec = _codec_registry.find_request_codec
find_request_codec_by_payload = _codec_registry.find_request_codec_by_payload
find_request_codec_by_type_hint = _codec_registry.find_request_codec_by_type_hint
find_input_codec = _codec_registry.find_input_codec
find_input_codec_by_payload = _codec_registry.find_input_codec_by_payload
find_input_codec_by_type_hint = _codec_registry.find_input_codec_by_type_hint


def register_request_codec(CodecKlass: RequestCodecLike):
    if CodecKlass.ContentType is not None:
        _codec_registry.register_request_codec(CodecKlass.ContentType, CodecKlass)
    return CodecKlass


def register_input_codec(CodecKlass: InputCodecLike):
    if CodecKlass.ContentType is not None:
        _codec_registry.register_input_codec(CodecKlass.ContentType, CodecKlass)
    return CodecKlass
