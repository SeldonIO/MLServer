import asyncio
from typing import AsyncIterator
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import StringCodec


class TextModel(MLModel):
    async def generate(self, payload: InferenceRequest) -> InferenceResponse:
        text = StringCodec.decode_input(payload.inputs[0])[0]
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
        text = StringCodec.decode_input(payload.inputs[0])[0]
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
