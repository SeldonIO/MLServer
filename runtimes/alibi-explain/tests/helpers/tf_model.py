import os
from pathlib import Path

import tensorflow as tf
from tensorflow.keras.layers import Activation, Conv2D, Dense, Dropout
from tensorflow.keras.layers import Flatten, Input, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse


_MODEL_PATH = Path(os.path.dirname(__file__)).parent / ".data" / "tf_mnist" / "model.h5"


def get_tf_mnist_model_uri() -> Path:
    if not _MODEL_PATH.exists():
        _train_tf_mnist()
    return _MODEL_PATH


class TFMNISTModel(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        np_codec = NumpyCodec
        model_input = payload.inputs[0]
        input_data = np_codec.decode_input(model_input)
        output_data = self._model(input_data).numpy()
        return InferenceResponse(
            model_name=self.name,
            outputs=[np_codec.encode_output("predict", output_data)],
        )

    async def load(self) -> bool:
        self._model = tf.keras.models.load_model(get_tf_mnist_model_uri())
        return True


def _train_tf_mnist() -> None:
    train, test = tf.keras.datasets.mnist.load_data()
    X_train, y_train = train
    X_test, y_test = test

    X_train = X_train.reshape(-1, 28, 28, 1).astype("float64") / 255
    X_test = X_test.reshape(-1, 28, 28, 1).astype("float64") / 255
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    inputs = Input(shape=(X_train.shape[1:]), dtype=tf.float64)
    x = Conv2D(64, 2, padding="same", activation="relu")(inputs)
    x = MaxPooling2D(pool_size=2)(x)
    x = Dropout(0.3)(x)

    x = Conv2D(32, 2, padding="same", activation="relu")(x)
    x = MaxPooling2D(pool_size=2)(x)
    x = Dropout(0.3)(x)

    x = Flatten()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    logits = Dense(10, name="logits")(x)
    outputs = Activation("softmax", name="softmax")(logits)

    model = Model(inputs=inputs, outputs=outputs)
    model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )

    # train model
    model.fit(
        X_train,
        y_train,
        epochs=6,
        batch_size=256,
        verbose=1,
        validation_data=(X_test, y_test),
    )

    _MODEL_PATH.parent.mkdir(parents=True)
    model.save(_MODEL_PATH, save_format="h5")
