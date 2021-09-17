from typing import Any

import orjson
from fastapi import Request, Response
from pydantic import BaseSettings

from mlserver.codecs import NumpyCodec
from mlserver.errors import InferenceError
from mlserver.handlers import custom_handler
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse


class AlibiExplainRuntimeBase(MLModel):
    """
    Base class for Alibi-Explain models
    """

    def __init__(self, settings: ModelSettings, explainer_settings: BaseSettings):

        self.alibi_explain_settings = explainer_settings
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

