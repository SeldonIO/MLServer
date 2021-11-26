from xgboost import DMatrix

from mlserver.codecs import NumpyCodec, register_input_codec, register_request_codec
from mlserver.codecs.utils import FirstInputRequestCodec
from mlserver.types import RequestInput
from mlserver.errors import InferenceError


@register_input_codec
class DMatrixCodec(NumpyCodec):
    ContentType = "dmatrix"

    @classmethod
    def decode(cls, request_input: RequestInput) -> DMatrix:  # type: ignore
        try:
            ndarray = super().decode(request_input)
            return DMatrix(ndarray)
        except Exception as e:
            # There are a few things that can go wrong here, e.g. less than 2-D
            # in the array), or input data not compatible with a numpy array
            raise InferenceError("Invalid input to XGBoostModel") from e


@register_request_codec
class DMatrixRequestCodec(FirstInputRequestCodec):
    InputCodec = DMatrixCodec
    ContentType = DMatrixCodec.ContentType
