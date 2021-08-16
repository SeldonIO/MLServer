import pickle
from mlserver_alibi_detect import AlibiDetector
from mlserver.utils import get_model_uri
from alibi_detect.cd import TabularDrift

DefaultPValue = 0.05


class TabularDriftDetector(AlibiDetector):
    """
    Implementation of the MLModel interface to load and serve Tabular drift models.
    """

    async def load(self) -> bool:
        super().load()

        model_uri = await get_model_uri(self._settings)
        ref_data = pickle.load(open(model_uri, "rb"))

        p_val = self._settings.parameters.initParameters.get("p_val", DefaultPValue)
        category_map = self._settings.parameters.initParameters.get(
            "categories_per_feature", {}
        )
        categories_per_feature = {
            int(f): category_map[f] for f in list(category_map.keys())
        }

        self._model = TabularDrift(ref_data, p_val, categories_per_feature)

        self.ready = True
        return self.ready
