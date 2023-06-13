import asyncio
import random
import string
import numpy as np

try:
    # NOTE: This is used in the EnvModel down below, which tests dynamic
    # loading custom environments.
    # Therefore, it is expected (and alright) that this package is not present
    # some times.
    import sklearn
except ImportError:
    sklearn = None

from typing import Dict, List

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.codecs import NumpyCodec, decode_args, StringCodec
from mlserver.handlers.custom import custom_handler
from mlserver.errors import MLServerError


class SumModel(MLModel):
    @custom_handler(rest_path="/my-custom-endpoint")
    async def my_payload(self, payload: list) -> int:
        return sum(payload)

    @custom_handler(rest_path="/custom-endpoint-with-long-response")
    async def long_response_endpoint(self, length: int) -> Dict[str, str]:
        alphabet = string.ascii_lowercase
        response = "".join(random.choice(alphabet) for i in range(length))
        return {"foo": response}

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode(payload.inputs[0])
        total = decoded.sum(axis=1, keepdims=True)

        output = NumpyCodec.encode_output(name="total", payload=total)
        response = InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[output],
        )

        if payload.parameters and payload.parameters.headers:
            # "Echo" headers back prefixed by `x-`
            request_headers = payload.parameters.headers
            response_headers = {}
            for header_name, header_value in request_headers.items():
                if header_name.startswith("x-"):
                    response_headers[header_name] = header_value

            response.parameters = Parameters(headers=response_headers)

        return response


class ErrorModel(MLModel):
    error_message = "something really bad happened"

    async def load(self) -> bool:
        if self._settings.parameters:
            load_error = getattr(self._settings.parameters, "load_error", False)
            if load_error:
                raise MLServerError(self.error_message)

        return True

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise MLServerError(self.error_message)


class SimpleModel(MLModel):
    @decode_args
    async def predict(self, foo: np.ndarray, bar: List[str]) -> np.ndarray:
        return foo.sum(axis=1, keepdims=True)


class SlowModel(MLModel):
    async def load(self) -> bool:
        await asyncio.sleep(10)
        return True

    async def infer(self, payload: InferenceRequest) -> InferenceResponse:
        await asyncio.sleep(10)
        return InferenceResponse(id=payload.id, model_name=self.name, outputs=[])


class EnvModel(MLModel):
    async def load(self):
        self._sklearn_version = sklearn.__version__
        return True

    async def predict(self, inference_request: InferenceRequest) -> InferenceResponse:
        return InferenceResponse(
            model_name=self.name,
            outputs=[
                StringCodec.encode_output("sklearn_version", [self._sklearn_version]),
            ],
        )
