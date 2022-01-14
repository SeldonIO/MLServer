from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.codecs import NumpyCodec
from mlserver.handlers.custom import custom_handler


class SumModel(MLModel):
    @custom_handler(rest_path="/my-custom-endpoint")
    async def my_payload(self, payload: list) -> int:
        return sum(payload)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode(payload.inputs[0])
        total = decoded.sum(axis=1, keepdims=True)

        output = NumpyCodec.encode(name="total", payload=total)
        response = InferenceResponse(
            id=payload.id, model_name=self.name, outputs=[output]
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
