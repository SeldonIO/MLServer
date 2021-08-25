from mlserver.types import InferenceRequest
from mlserver.codecs import RequestCodec, register_request_codec, get_decoded_or_raw

from .encoding import TensorDict


@register_request_codec
class TensorDictCodec(RequestCodec):
    ContentType = "dict"

    @classmethod
    def decode(cls, request: InferenceRequest) -> TensorDict:
        return {
            request_input.name: get_decoded_or_raw(request_input)
            for request_input in request.inputs
        }
