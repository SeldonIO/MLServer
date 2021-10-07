import os
from pathlib import Path

import tensorflow as tf

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse


def get_tf_mnist_model_uri() -> Path:
    return Path(os.path.dirname(__file__)) / "data" / "tf_mnist" / "model.h5"


class TFMNISTModel(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        np_codec = NumpyCodec
        model_input = payload.inputs[0]
        input_data = np_codec.decode(model_input)
        output_data = self._model(input_data).numpy()
        return InferenceResponse(
            model_name=self.name,
            outputs=[np_codec.encode("predict", output_data)],
        )

    async def load(self) -> bool:
        self._model = tf.keras.models.load_model(get_tf_mnist_model_uri())
