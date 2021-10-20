"""
Dummy models which require a custom environment (either provided by an
environment.yml or a requirements.txt file).

Note that this is independent from the SKLearn runtime, and it's only meant to
be used to test custom model images.
"""

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import NumpyCodec
from mlserver.handlers.custom import custom_handler


class DummySKLearnModel(MLModel):
    async def load(self) -> bool:
        n = 4
        X = np.random.rand(n)
        y = np.random.rand(n)

        self._model = DummyClassifier(strategy="prior")
        self._model.fit(X, y)

        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode(payload.inputs[0])
        prediction = self._model.predict(decoded)

        output = NumpyCodec().encode(name="prediction", payload=total)
        return InferenceResponse(id=payload.id, model_name=self.name, outputs=[output])
