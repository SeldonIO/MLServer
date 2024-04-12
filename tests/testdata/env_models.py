"""
Dummy models which require a custom environment (either provided by an
environment.yml or a requirements.txt file).

Note that this is independent from the SKLearn runtime, and it's only meant to
be used to test custom model images.
"""

import numpy as np

from sklearn.dummy import DummyClassifier

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import NumpyRequestCodec


class DummySKLearnModel(MLModel):
    async def load(self) -> bool:
        n = 4
        X = np.random.rand(n)
        y = np.random.rand(n)

        self._model = DummyClassifier(strategy="prior")
        self._model.fit(X, y)

        return True

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)
        prediction = self._model.predict(decoded)

        return NumpyRequestCodec.encode_response(
            model_name=self.name, payload=prediction, model_version=self.version
        )
