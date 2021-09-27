import os
from typing import Any

import tensorflow as tf
from alibi.api.interfaces import Explanation
from alibi.explainers import IntegratedGradients
from pydantic import BaseSettings
from tensorflow.keras.layers import Activation, Conv2D, Dense, Dropout
from tensorflow.keras.layers import Flatten, Input, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

from mlserver import ModelSettings
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class IntegratedGradientsWrapper(AlibiExplainRuntimeBase):
    def __init__(self, settings: ModelSettings):
        self._inference_model = None

        explainer_settings = AlibiExplainSettings(**settings.parameters.extra)
        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        self._inference_model = _train_model("/tmp/tf_mnist")

        if self.settings.parameters.uri is None:
            init_parameters = self.alibi_explain_settings.init_parameters
            self._model = IntegratedGradients(
                model=self._inference_model,
                **init_parameters)
        # TODO: load the model from disk

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any, settings: BaseSettings) -> Explanation:
        # TODO: how are we going to deal with that?
        predictions = self._inference_model(input_data).numpy().argmax(axis=1)
        explain_parameters = settings.explain_parameters
        return self._model.explain(
            input_data,
            target=predictions,
            **explain_parameters
        )


def _train_model(filepath: str) -> Model:
    if not os.path.exists(filepath):
        os.makedirs(filepath)

        train, test = tf.keras.datasets.mnist.load_data()
        X_train, y_train = train
        X_test, y_test = test
        test_labels = y_test.copy()
        train_labels = y_train.copy()

        X_train = X_train.reshape(-1, 28, 28, 1).astype('float64') / 255
        X_test = X_test.reshape(-1, 28, 28, 1).astype('float64') / 255
        y_train = to_categorical(y_train, 10)
        y_test = to_categorical(y_test, 10)

        inputs = Input(shape=(X_train.shape[1:]), dtype=tf.float64)
        x = Conv2D(64, 2, padding='same', activation='relu')(inputs)
        x = MaxPooling2D(pool_size=2)(x)
        x = Dropout(.3)(x)

        x = Conv2D(32, 2, padding='same', activation='relu')(x)
        x = MaxPooling2D(pool_size=2)(x)
        x = Dropout(.3)(x)

        x = Flatten()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(.5)(x)
        logits = Dense(10, name='logits')(x)
        outputs = Activation('softmax', name='softmax')(logits)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        # train model
        model.fit(X_train,
                  y_train,
                  epochs=6,
                  batch_size=256,
                  verbose=1,
                  validation_data=(X_test, y_test)
                  )

        model.save(os.path.join(filepath, 'model.h5'))

    persisted_model = tf.keras.models.load_model(
        os.path.join(filepath, 'model.h5'))

    return persisted_model
