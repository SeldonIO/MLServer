import asyncio
import json
import os
from pathlib import Path
from typing import AsyncIterable
from unittest.mock import patch

import tensorflow as tf

import nest_asyncio
import pytest
from alibi.explainers import AnchorImage
from fastapi import FastAPI
from fastapi.testclient import TestClient

from mlserver import MLModel
from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.registry import MultiModelRegistry
from mlserver.repository import ModelRepository
from mlserver.rest import RESTServer
from mlserver.settings import ModelSettings, ModelParameters, Settings
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntime
from helpers.tf_model import TFMNISTModel, get_tf_mnist_model_uri

# allow nesting loop
# in our case this allows multiple runtimes to execute
# in the same thread for testing reasons
nest_asyncio.apply()

TESTS_PATH = Path(os.path.dirname(__file__))
_ANCHOR_IMAGE_DIR = TESTS_PATH / "data" / "mnist_anchor_image"


# TODO: how to make this in utils?
def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
async def custom_runtime_tf() -> MLModel:
    model = TFMNISTModel(
        ModelSettings(
            name="custom_tf_mnist_model",
            implementation="helpers.tf_model.TFMNISTModel",
        )
    )
    await model.load()

    return model


@pytest.fixture
def settings() -> Settings:
    return Settings(debug=True, host="127.0.0.1")


@pytest.fixture
async def model_registry(custom_runtime_tf) -> MultiModelRegistry:
    model_registry = MultiModelRegistry()
    await model_registry.load(custom_runtime_tf)
    return model_registry


@pytest.fixture
def data_plane(settings: Settings, model_registry: MultiModelRegistry) -> DataPlane:
    return DataPlane(settings=settings, model_registry=model_registry)


@pytest.fixture
def model_repository(tmp_path, custom_runtime_tf) -> ModelRepository:
    model_settings_path = tmp_path.joinpath("model-settings.json")
    impl = custom_runtime_tf.settings.implementation
    model_settings_dict = {
        "name": custom_runtime_tf.settings.name,
        "implementation": f"{impl.__module__}.{impl.__name__}",
        "parallel_workers": 0,
    }

    model_settings_path.write_text(json.dumps(model_settings_dict, indent=4))
    return ModelRepository(tmp_path)


@pytest.fixture
def model_repository_handlers(
    model_repository: ModelRepository, model_registry: MultiModelRegistry
) -> ModelRepositoryHandlers:
    return ModelRepositoryHandlers(
        repository=model_repository, model_registry=model_registry
    )


@pytest.fixture
async def rest_server(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    custom_runtime_tf: MLModel,
) -> AsyncIterable[RESTServer]:
    server = RESTServer(
        settings=settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    await asyncio.gather(server.add_custom_handlers(custom_runtime_tf))

    yield server

    await asyncio.gather(server.delete_custom_handlers(custom_runtime_tf))


@pytest.fixture
def rest_app(rest_server: RESTServer) -> FastAPI:
    return rest_server._app


@pytest.fixture
def rest_client(rest_app: FastAPI) -> TestClient:
    return TestClient(rest_app)


@pytest.fixture
def anchor_image_directory() -> Path:
    if not _ANCHOR_IMAGE_DIR.exists():
        _train_anchor_image_explainer()
    return _ANCHOR_IMAGE_DIR


@pytest.fixture
async def anchor_image_runtime_with_remote_predict_patch(
    anchor_image_directory,
    custom_runtime_tf: MLModel,
    remote_predict_mock_path: str = "mlserver_alibi_explain.common.remote_predict",
) -> AlibiExplainRuntime:
    with patch(remote_predict_mock_path) as remote_predict:

        def mock_predict(*args, **kwargs):
            # note: sometimes the event loop is not running and in this case
            # we create a new one otherwise
            # we use the existing one.
            # this mock implementation is required as we dont want to spin up a server,
            # we just use MLModel.predict
            try:
                loop = asyncio.get_event_loop()
                res = loop.run_until_complete(
                    custom_runtime_tf.predict(kwargs["v2_payload"])
                )
                return res
            except Exception:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res = loop.run_until_complete(
                    custom_runtime_tf.predict(kwargs["v2_payload"])
                )
                return res

        remote_predict.side_effect = mock_predict

        rt = AlibiExplainRuntime(
            ModelSettings(
                parallel_workers=0,
                parameters=ModelParameters(
                    uri=str(anchor_image_directory),
                    extra=AlibiExplainSettings(
                        explainer_type="anchor_image", infer_uri="dummy_call"
                    ),
                ),
            )
        )
        await rt.load()

        return rt


@pytest.fixture
async def integrated_gradients_runtime() -> AlibiExplainRuntime:
    rt = AlibiExplainRuntime(
        ModelSettings(
            parallel_workers=1,
            parameters=ModelParameters(
                extra=AlibiExplainSettings(
                    init_parameters={"n_steps": 50, "method": "gausslegendre"},
                    explainer_type="integrated_gradients",
                    infer_uri=str(get_tf_mnist_model_uri()),
                )
            ),
        )
    )
    await rt.load()

    return rt


def _train_anchor_image_explainer() -> None:
    model = tf.keras.models.load_model(get_tf_mnist_model_uri())
    anchor_image = AnchorImage(model.predict, (28, 28, 1))

    _ANCHOR_IMAGE_DIR.mkdir(parents=True)
    anchor_image.save(_ANCHOR_IMAGE_DIR)
