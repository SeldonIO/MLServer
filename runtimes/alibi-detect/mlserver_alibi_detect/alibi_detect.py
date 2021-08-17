from mlserver import types
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.codecs import NumpyCodec
from fastapi import Request, Response
from mlserver.handlers import custom_handler
from .protocols.util import (
    NumpyEncoder,
    get_request_handler,
    Protocol,
)
import numpy as np
import json
from typing import Optional


def getPredictParams(
    parameters: dict, payloadParameters: Optional[types.Parameters] = None
) -> dict:
    if payloadParameters is not None:
        return {
            **parameters,
            **{
                f: payloadParameters.__getattribute__(f)
                for f in list(parameters.keys())
            },
        }
    return parameters


class AlibiDetector(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):

        self.protocol = Protocol(settings.parameters.initParameters["protocol"])
        super().__init__(settings)

    @custom_handler(rest_path="/")
    async def invocations(self, request: Request) -> Response:
        """
        This custom handler is meant to mimic the behaviour prediction in alibi-detect
        """
        raw_data = await request.body()
        as_str = raw_data.decode("utf-8")

        try:
            body = json.loads(as_str)
        except json.decoder.JSONDecodeError as e:
            raise InferenceError("Unrecognized request format: %s" % e)

        request_handler = get_request_handler(self.protocol, body)
        request_handler.validate()
        input_data = request_handler.extract_request()

        y = self._model.predict(
            input_data, **getPredictParams(self._settings.parameters.predictParameters)
        )
        output_data = json.dumps(y, cls=NumpyEncoder)
        return Response(content=output_data, media_type="application/json")

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        model_input = self._check_request(payload)

        default_codec = NumpyCodec()
        input_data = self.decode(model_input, default_codec=default_codec)

        y = self._model.predict(
            input_data,
            **getPredictParams(
                self._settings.parameters.predictParameters, payload.parameters
            ),
        )
        # TODO: Convert alibi-detect output to v2 protocol
        output_data = np.array(y["data"]["is_drift"])

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=[default_codec.encode(name="detect", payload=output_data)],
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "AlibiDetector only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )
        return payload.inputs[0]
