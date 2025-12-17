import tensorflow as tf

from tensorflow.keras.layers import Activation, Conv2D, Dense, Dropout
from tensorflow.keras.layers import Flatten, Input, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

from mlserver import MLModel
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse


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
        model_uri = await get_model_uri(self._settings)
        self._model = tf.keras.models.load_model(model_uri)
        return True


def train_tf_mnist(model_h5_uri: str) -> None:
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

    model.save(model_h5_uri, save_format="h5")
