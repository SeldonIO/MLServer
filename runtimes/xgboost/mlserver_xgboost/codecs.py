from xgboost import DMatrix

from mlserver.codecs import NumpyCodec
from mlserver.types import RequestInput
from mlserver.errors import InferenceError


class DMatrixCodec(NumpyCodec):
    def decode(self, request_input: RequestInput) -> DMatrix:  # type: ignore
        try:
            ndarray = super().decode(request_input)
            return DMatrix(ndarray)
        except Exception as e:
            # There are a few things that can go wrong here, e.g. less than 2-D
            # in the array), or input data not compatible with a numpy array
            raise InferenceError("Invalid input to XGBoostModel") from e
