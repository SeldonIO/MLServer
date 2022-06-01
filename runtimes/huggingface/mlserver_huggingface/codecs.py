from typing import Optional, Type, Any, Dict
from mlserver.codecs.utils import (
    has_decoded,
    _save_decoded,
    get_decoded_or_raw,
)
from mlserver.codecs.base import (
    RequestCodec,
    register_request_codec,
    InputCodec as InputCodecTy,
)
from mlserver.codecs import StringCodec
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)


class MultiInputRequestCodec(RequestCodec):
    """
    The SingleInputRequestCodec can be used as a "meta-implementation" for other
    codecs. Its goal to decode the whole request simply as the first decoded
    element.
    """

    InputCodec: Optional[Type[InputCodecTy]] = None

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        if cls.InputCodec is None:
            return False

        return cls.InputCodec.can_encode(payload)

    @classmethod
    def encode_response(
        cls,
        model_name: str,
        payload: Dict[str, Any],
        model_version: Optional[str] = None,
        **kwargs
    ) -> InferenceResponse:
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            outputs=[
                cls.InputCodec.encode_output(key, value, **kwargs)  # type: ignore
                for key, value in payload.items()
            ],
        )

    @classmethod
    def decode_response(cls, response: InferenceResponse) -> Dict[str, Any]:
        values = {}
        for item in response.outputs:
            if not has_decoded(item) and cls.InputCodec is not None:
                decoded_payload = cls.InputCodec.decode_output(item)  # type: ignore
                _save_decoded(item, decoded_payload)

            value = get_decoded_or_raw(item)
            values[item.name] = value
        return values

    @classmethod
    def encode_request(cls, payload: Dict[str, Any], **kwargs) -> InferenceRequest:
        return InferenceRequest(
            inputs=[
                cls.InputCodec.encode_input(key, value, **kwargs)  # type: ignore
                for key, value in payload.items()
            ],
        )

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> Dict[str, Any]:
        values = {}
        for item in request.inputs:
            if not has_decoded(item) and cls.InputCodec is not None:
                decoded_payload = cls.InputCodec.decode_input(item)  # type: ignore
                _save_decoded(item, decoded_payload)

            value = get_decoded_or_raw(item)
            values[item.name] = value
        return values


@register_request_codec
class MultiStringRequestCodec(MultiInputRequestCodec):
    InputCodec = StringCodec
    ContentType = StringCodec.ContentType
