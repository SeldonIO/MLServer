import mlflow

from mlserver import types
from mlserver.model import MLModel
from mlserver.utils import get_model_uri


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

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        return types.InferenceResponse(
            model_name=self.name, model_version=self.version, outputs=[]
        )
