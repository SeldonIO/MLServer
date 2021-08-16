import pickle
from mlserver_alibi_detect import AlibiDetector
from mlserver.utils import get_model_uri
from alibi_detect.cd import ChiSquareDrift

DefaultPValue = 0.05


class ChiSquareDriftDetector(AlibiDetector):
    """
    Implementation of the MLModel interface to load and serve Tabular drift models.
    """

    async def load(self) -> bool:
        super().load()

        model_uri = await get_model_uri(self._settings)
        ref_data = pickle.load(open(model_uri, "rb"))

        p_val = self._settings.parameters.initParameters.get("p_val", DefaultPValue)

        self._model = ChiSquareDrift(ref_data, p_val)

        self.ready = True
        return self.ready
