from xgboost import DMatrix

from mlserver.codecs import NumpyCodec
from mlserver.types import RequestInput


class DMatrixCodec(NumpyCodec):
    def decode(self, request_input: RequestInput) -> DMatrix:
        ndarray = super().decode(request_input)
        return DMatrix(ndarray)
