import asyncio
from typing import AsyncIterator
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import StringCodec


class TextModel(MLModel):

    async def predict_stream(
        self, payloads: AsyncIterator[InferenceRequest]
    ) -> AsyncIterator[InferenceResponse]:
        payload = [_ async for _ in payloads][0]
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
