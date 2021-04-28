import mlflow

from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.model import MLModel
from mlserver.utils import get_model_uri

from .encoding import to_tensor_dict, to_outputs


class MLflowRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `scikit-learn`
    models persisted with `joblib`.
    """

    async def load(self) -> bool:
        # TODO: Log info message
        model_uri = await get_model_uri(self._settings)
        self._model = mlflow.pyfunc.load_model(model_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        tensor_dict = to_tensor_dict(payload.inputs)

        # TODO: Can `output` be a dictionary of tensors?
        model_output = self._model.predict(tensor_dict)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=to_outputs(model_output),
        )
