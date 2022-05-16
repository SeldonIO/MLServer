from typing import Optional, Type, Any
from mlserver.codecs.utils import has_decoded, _save_decoded, get_decoded_or_raw
from mlserver.codecs.base import (
    RequestCodec,
    register_request_codec,
    InputCodec as InputCodecTy,
)
from mlserver.codecs import (
    StringCodec,
)
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
    def encode(
        cls, model_name: str, payload: Any, model_version: Optional[str] = None
    ) -> InferenceResponse:
        raise NotImplementedError()

    @classmethod
    def decode(cls, request: InferenceRequest) -> Any:
        values = {}
        for item in request.inputs:
            if not has_decoded(item) and cls.InputCodec is not None:
                decoded_payload = cls.InputCodec.decode(item)  # type: ignore
                _save_decoded(item, decoded_payload)

            value = get_decoded_or_raw(item)
            values[item.name] = value
        return values


@register_request_codec
class MultiStringRequestCodec(MultiInputRequestCodec):
    InputCodec = StringCodec
    ContentType = StringCodec.ContentType
