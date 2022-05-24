import json
import pytest
import os
import shutil
import asyncio

from unittest.mock import Mock
from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.registry import MultiModelRegistry
from mlserver.repository import ModelRepository, DEFAULT_MODEL_SETTINGS_FILENAME
from mlserver.parallel import InferencePool
from mlserver.utils import install_uvloop_event_loop
from mlserver import types, Settings, ModelSettings

from .fixtures import SumModel, ErrorModel
from .helpers import get_import_path

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


def assert_not_called_with(self, *args, **kwargs):
    """
    From https://stackoverflow.com/a/54838760/5015573
    """
    try:
        self.assert_called_with(*args, **kwargs)
    except AssertionError:
        return
    raise AssertionError(
        "Expected %s to not have been called."
        % self._format_mock_call_signature(args, kwargs)
    )


Mock.assert_not_called_with = assert_not_called_with


@pytest.fixture
def event_loop():
    # By default use uvloop for tests
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sum_model_settings() -> ModelSettings:
    model_settings_path = os.path.join(TESTDATA_PATH, "model-settings.json")
    return ModelSettings.parse_file(model_settings_path)


@pytest.fixture
def error_model_settings() -> ModelSettings:
    model_settings_path = os.path.join(TESTDATA_PATH, "model-settings.json")
    model_settings = ModelSettings.parse_file(model_settings_path)
    model_settings.name = "error-model"
    model_settings.implementation = ErrorModel
    return model_settings


@pytest.fixture
async def error_model(
    model_registry: MultiModelRegistry, error_model_settings: ModelSettings
) -> ErrorModel:
    await model_registry.load(error_model_settings)
    return await model_registry.get_model(error_model_settings.name)


@pytest.fixture
async def sum_model(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
) -> SumModel:
    return await model_registry.get_model(sum_model_settings.name)


@pytest.fixture
def metadata_server_response() -> types.MetadataServerResponse:
    payload_path = os.path.join(TESTDATA_PATH, "metadata-server-response.json")
    return types.MetadataServerResponse.parse_file(payload_path)


@pytest.fixture
def metadata_model_response() -> types.MetadataModelResponse:
    payload_path = os.path.join(TESTDATA_PATH, "metadata-model-response.json")
    return types.MetadataModelResponse.parse_file(payload_path)


@pytest.fixture(params=["inference-request.json", "inference-request-with-output.json"])
def inference_request(request) -> types.InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, request.param)
    return types.InferenceRequest.parse_file(payload_path)


@pytest.fixture(
    params=["inference-response.json", "inference-response-with-output.json"]
)
def inference_response(request) -> types.InferenceResponse:
    payload_path = os.path.join(TESTDATA_PATH, request.param)
    return types.InferenceResponse.parse_file(payload_path)


@pytest.fixture
async def model_registry(sum_model_settings: ModelSettings) -> MultiModelRegistry:
    model_registry = MultiModelRegistry()
    await model_registry.load(sum_model_settings)
    return model_registry


@pytest.fixture
def settings() -> Settings:
    settings_path = os.path.join(TESTDATA_PATH, "settings.json")
    return Settings.parse_file(settings_path)


@pytest.fixture
def data_plane(settings: Settings, model_registry: MultiModelRegistry) -> DataPlane:
    return DataPlane(settings=settings, model_registry=model_registry)


@pytest.fixture
def model_repository_handlers(
    model_repository: ModelRepository, model_registry: MultiModelRegistry
) -> ModelRepositoryHandlers:
    return ModelRepositoryHandlers(
        repository=model_repository, model_registry=model_registry
    )


@pytest.fixture
def model_folder(tmp_path):
    to_copy = ["model-settings.json"]

    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = tmp_path.joinpath(file_name)
        shutil.copyfile(src, dst)

    return tmp_path


@pytest.fixture
def multi_model_folder(model_folder, sum_model_settings):
    # Remove original
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    os.remove(model_settings_path)

    num_models = 5
    for idx in range(num_models):
        sum_model_settings.parameters.version = f"v{idx}"

        model_version_folder = os.path.join(
            model_folder,
            "sum-model",
            sum_model_settings.parameters.version,
        )
        os.makedirs(model_version_folder)

        model_settings_path = os.path.join(
            model_version_folder, DEFAULT_MODEL_SETTINGS_FILENAME
        )
        with open(model_settings_path, "w") as f:
            settings_dict = sum_model_settings.dict()
            settings_dict["implementation"] = get_import_path(
                sum_model_settings.implementation
            )
            f.write(json.dumps(settings_dict))

    return model_folder


@pytest.fixture
def model_repository(model_folder: str) -> ModelRepository:
    return ModelRepository(model_folder)


@pytest.fixture
def repository_index_request() -> types.RepositoryIndexRequest:
    return types.RepositoryIndexRequest(ready=None)


@pytest.fixture
def repository_index_response(sum_model_settings) -> types.RepositoryIndexResponse:
    return types.RepositoryIndexResponse(
        __root__=[
            types.RepositoryIndexResponseItem(
                name=sum_model_settings.name,
                version=sum_model_settings.parameters.version,
                state=types.State.READY,
                reason="",
            ),
        ]
    )


@pytest.fixture
async def inference_pool(settings: Settings) -> InferencePool:
    pool = InferencePool(settings)
    yield pool

    await pool.close()
