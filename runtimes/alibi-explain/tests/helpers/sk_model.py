import os
from pathlib import Path
import joblib

from sklearn.ensemble import GradientBoostingClassifier
from alibi.datasets import fetch_adult

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse


_MODEL_PATH = Path(os.path.dirname(__file__)).parent / ".data" / "sk_income" / "model.joblib"


def get_sk_income_model_uri() -> Path:
    if not _MODEL_PATH.exists():
        _train_sk_income()
    return _MODEL_PATH


class SKIncomeModel(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        np_codec = NumpyCodec
        model_input = payload.inputs[0]
        input_data = np_codec.decode_input(model_input)
        output_data = self._model(input_data)
        return InferenceResponse(
            model_name=self.name,
            outputs=[np_codec.encode_output("predict", output_data)]
        )

    async def load(self) -> bool:
        self._model = joblib.load(get_sk_income_model_uri())
        return True


def _train_sk_income() -> None:
    data = get_income_data()
    X_train, Y_train = data['X'], data['Y']

    model = GradientBoostingClassifier(n_estimators=50)
    model.fit(X_train, Y_train)

    _MODEL_PATH.parent.mkdir(parents=True)
    joblib.dump(model, _MODEL_PATH)


def get_income_data() -> dict:
    print('Generating adult dataset...')
    adult = fetch_adult()
    X = adult.data
    Y = adult.target

    feature_names = adult.feature_names
    category_map = adult.category_map

    # Package into dictionary
    data_dict = {
        'X': X,
        'Y': Y,
        'feature_names': feature_names,
        'category_map': category_map,
        'target_names': adult.target_names,
    }
    return data_dict
