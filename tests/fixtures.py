import asyncio
import random
import string

import numpy as np
from fastapi import Body

try:
    # NOTE: This is used in the EnvModel down below, which tests dynamic
    # loading custom environments.
    # Therefore, it is expected (and alright) that this package is not present
    # some times.
    import sklearn
except ImportError:
    sklearn = None

from typing import Dict, List, AsyncIterator

from mlserver import MLModel
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    ResponseOutput,
    Parameters,
)
from mlserver.codecs import NumpyRequestCodec, NumpyCodec, decode_args, StringCodec
from mlserver.handlers.custom import custom_handler
from mlserver.errors import MLServerError


class SumModel(MLModel):
    @custom_handler(rest_path="/my-custom-endpoint")
    async def my_payload(self, payload: list = Body(...)) -> int:
        return sum(payload)

    @custom_handler(rest_path="/custom-endpoint-with-long-response")
    async def long_response_endpoint(self, length: int = Body(...)) -> Dict[str, str]:
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


class TextStreamModel(MLModel):
    async def generate(self, payload: InferenceRequest) -> InferenceResponse:
        text = "Hey now brown cow"
        return InferenceResponse(
            model_name=self._settings.name,
            outputs=[
                StringCodec.encode_output(
                    name="output",
                    payload=[text],
                    use_bytes=True,
                ),
            ],
        )

    async def generate_stream(
        self, payload: InferenceRequest
    ) -> AsyncIterator[InferenceResponse]:
        text = "Hey now brown cow"
        words = text.split(" ")

        split_text = []
        for i, word in enumerate(words):
            split_text.append(word if i == 0 else " " + word)

        for word in split_text:
            await asyncio.sleep(0.5)
            yield InferenceResponse(
                model_name=self._settings.name,
                outputs=[
                    StringCodec.encode_output(
                        name="output",
                        payload=[word],
                        use_bytes=True,
                    ),
                ],
            )


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


class EchoModel(MLModel):
    async def load(self) -> bool:
        print("Echo Model Initialized")
        return await super().load()

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        return InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                ResponseOutput(
                    name=input.name,
                    shape=input.shape,
                    datatype=input.datatype,
                    data=input.data,
                    parameters=input.parameters,
                )
                for input in payload.inputs
            ],
        )
