from mlserver import types
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.codecs import NumpyCodec
from fastapi import Request, Response
from mlserver.handlers import custom_handler
from .protocols.util import (
    get_request_handler,
    Protocol,
)
import numpy as np
import orjson
from typing import Optional, Any
from pydantic import BaseSettings, PyObject

ENV_PREFIX_ALIBI_DETECT_SETTINGS = "MLSERVER_MODEL_ALIBI_DETECT_"


class AlibiDetectSettings(BaseSettings):
    """
    Parameters that apply only to alibi detect models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_DETECT_SETTINGS

    init_detector: bool = False
    detector_type: PyObject = ""
    protocol: Optional[str] = "seldon.http"
    init_parameters: Optional[dict] = {}
    predict_parameters: Optional[dict] = {}


class AlibiDetectParameters(BaseSettings):
    """
    Parameters that apply only to alibi detect models
    """

    predict_parameters: Optional[dict] = {}


class AlibiDetectRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):

        self.alibi_detect_settings = AlibiDetectSettings(**settings.parameters.extra)
        super().__init__(settings)

    @custom_handler(rest_path="/")
    async def detect(self, request: Request) -> Response:
        """
        This custom handler is meant to mimic the behaviour prediction in alibi-detect
        """
        raw_data = await request.body()
        as_str = raw_data.decode("utf-8")

        try:
            body = orjson.loads(as_str)
        except orjson.JSONDecodeError as e:
            raise InferenceError("Unrecognized request format: %s" % e)

        request_handler = get_request_handler(
            Protocol(self.alibi_detect_settings.protocol), body
        )
        request_handler.validate()
        input_data = request_handler.extract_request()

        y = await self.predict_fn(input_data)
        output_data = orjson.dumps(y, option=orjson.OPT_SERIALIZE_NUMPY)

        return Response(content=output_data, media_type="application/json")

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)
        model_input = payload.inputs[0]
        default_codec = NumpyCodec()
        input_data = self.decode(model_input, default_codec=default_codec)
        y = await self.predict_fn(input_data)

        # TODO: Convert alibi-detect output to v2 protocol
        output_data = np.array(y["data"])

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=[default_codec.encode(name="detect", payload=output_data)],
        )

    async def predict_fn(self, input_data: Any) -> dict:
        parameters = self.alibi_detect_settings.predict_parameters
        return self._model.predict(input_data, **parameters)

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "AlibiDetector only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )
        return payload
