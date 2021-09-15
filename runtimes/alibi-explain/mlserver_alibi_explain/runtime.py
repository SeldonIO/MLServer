from typing import Any, Optional

import orjson
from fastapi import Request, Response
from pydantic import BaseSettings

from mlserver.codecs import NumpyCodec
from mlserver.errors import InferenceError
from mlserver.handlers import custom_handler
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse

ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    # TODO: add more structure?
    predict_parameters: Optional[dict] = {}


class AlibiExplainRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):

        self.alibi_explain_settings = AlibiExplainSettings(**settings.parameters.extra)
        super().__init__(settings)

    @custom_handler(rest_path="/")
    async def explain(self, request: Request) -> Response:  # TODO: add Explain request
        """
        This custom handler serves specific alibi explain model
        """
        raw_data = await request.body()
        as_str = raw_data.decode("utf-8")

        try:
            body = orjson.loads(as_str)
        except orjson.JSONDecodeError as e:
            raise InferenceError("Unrecognized request format: %s" % e)

        # TODO: convert and validate
        input_data = body

        y = await self.predict_fn(input_data)
        output_data = orjson.dumps(y, option=orjson.OPT_SERIALIZE_NUMPY)

        return Response(content=output_data, media_type="application/json")

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:

        # TODO: convert and validate
        model_input = payload.inputs[0]
        default_codec = NumpyCodec()
        input_data = self.decode(model_input, default_codec=default_codec)
        y = await self.predict_fn(input_data)

        # TODO: Convert alibi-explain output to v2 protocol
        output_data = y

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[default_codec.encode(name="explain", payload=output_data)],
        )

    async def predict_fn(self, input_data: Any) -> dict:
        parameters = self.alibi_explain_settings.predict_parameters
        return self._model.predict(input_data, **parameters)
