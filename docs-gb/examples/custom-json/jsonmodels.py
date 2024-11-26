import json

from typing import Dict, Any
from mlserver import MLModel, types
from mlserver.codecs import StringCodec


class JsonHelloWorldModel(MLModel):
    async def load(self) -> bool:
        # Perform additional custom initialization here.
        print("Initialize model")

        # Set readiness flag for model
        return await super().load()

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        request = self._extract_json(payload)
        response = {
            "request": request,
            "server_response": "Got your request. Hello from the server.",
        }
        response_bytes = json.dumps(response).encode("UTF-8")

        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name="echo_response",
                    shape=[len(response_bytes)],
                    datatype="BYTES",
                    data=[response_bytes],
                    parameters=types.Parameters(content_type="str"),
                )
            ],
        )

    def _extract_json(self, payload: types.InferenceRequest) -> Dict[str, Any]:
        inputs = {}
        for inp in payload.inputs:
            inputs[inp.name] = json.loads(
                "".join(self.decode(inp, default_codec=StringCodec))
            )

        return inputs
