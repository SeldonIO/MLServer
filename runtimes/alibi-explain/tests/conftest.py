import os

import pytest
from keras.models import load_model
from tensorflow.python.keras.applications.inception_v3 import InceptionV3

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.utils import get_model_uri
from mlserver_alibi_explain import AlibiExplainRuntime

TESTS_PATH = os.path.dirname(__file__)


# TODO: how to make this in utils?
def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
def model_uri_imagenet(tmp_path) -> str:
    model = InceptionV3(weights='imagenet')
    model_path = os.path.join(tmp_path, "imagenet-model")
    model.save(filepath=model_path)

    return model_path


@pytest.fixture
def model_settings(model_uri_imagenet: str) -> ModelSettings:
    return ModelSettings(
        name="alibi-explain-model",
        parameters=ModelParameters(uri=model_uri_imagenet),
    )


@pytest.fixture
async def runtime(model_settings: ModelSettings) -> AlibiExplainRuntime:
    # TODO: what options do we have here?
    class AlibiExplainInstance(AlibiExplainRuntime):
        async def load(self) -> bool:
            model_uri = await get_model_uri(self._settings)

            # TODO: how to sort this out for different models?
            self._model = load_model(model_uri)

            # TODO: this should be in the base impl?
            self.ready = True
            return self.ready

    rt = AlibiExplainInstance(model_settings)
    await rt.load()

    return rt

