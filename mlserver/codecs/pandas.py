# TODO: Should we make Pandas optional?
import pandas as pd

from .base import RequestCodec, register_request_codec
from ..types import InferenceRequest, InferenceResponse


@register_request_codec
class PandasCodec(RequestCodec):
    ContentType = "pd"

    def encode(self, name: str, payload: pd.DataFrame) -> InferenceResponse:
        raise NotImplementedError()

    def decode(self, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: request_input.data for request_input in request.inputs
        }
        return pd.DataFrame(data)
