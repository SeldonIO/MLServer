import pytest
import os
import shutil
import asyncio
import glob
import json

from filelock import FileLock
from typing import Dict, Any, Tuple
from starlette_exporter import PrometheusMiddleware
from prometheus_client.registry import REGISTRY, CollectorRegistry
from unittest.mock import Mock

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.registry import MultiModelRegistry
from mlserver.repository import (
    ModelRepository,
    SchemalessModelRepository,
    DEFAULT_MODEL_SETTINGS_FILENAME,
)
from mlserver.parallel import InferencePoolRegistry
from mlserver.utils import install_uvloop_event_loop
from mlserver.logging import configure_logger
from mlserver.env import Environment
from mlserver.metrics.registry import MetricsRegistry, REGISTRY as METRICS_REGISTRY
from mlserver import types, Settings, ModelSettings, MLServer

from .metrics.utils import unregister_metrics
from .fixtures import SumModel, TextModel, ErrorModel, SimpleModel
from .utils import RESTClient, get_available_ports, _pack, _get_tarball_name

MIN_PYTHON_VERSION = (3, 9)
MAX_PYTHON_VERSION = (3, 10)
PYTHON_VERSIONS = [
    (major, minor)
    for major in range(MIN_PYTHON_VERSION[0], MAX_PYTHON_VERSION[0] + 1)
    for minor in range(MIN_PYTHON_VERSION[1], MAX_PYTHON_VERSION[1] + 1)
]
TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")
TESTDATA_CACHE_PATH = os.path.join(TESTDATA_PATH, ".cache")


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
def testdata_cache_path() -> str:
    if not os.path.exists(TESTDATA_CACHE_PATH):
        os.makedirs(TESTDATA_CACHE_PATH, exist_ok=True)

    return TESTDATA_CACHE_PATH


@pytest.fixture(
    params=PYTHON_VERSIONS,
    ids=[f"py{major}{minor}" for (major, minor) in PYTHON_VERSIONS],
)
def env_python_version(request: pytest.FixtureRequest) -> Tuple[int, int]:
    return request.param


@pytest.fixture
async def env_tarball(
    env_python_version: Tuple[int, int],
    testdata_cache_path: str,
) -> str:
    tarball_name = _get_tarball_name(env_python_version)
    tarball_path = os.path.join(testdata_cache_path, tarball_name)

    with FileLock(f"{tarball_path}.lock"):
        if os.path.isfile(tarball_path):
            return tarball_path

        env_yml = os.path.join(TESTDATA_PATH, "environment.yml")
        await _pack(env_python_version, env_yml, tarball_path)

    return tarball_path


@pytest.fixture
async def env(env_tarball: str, tmp_path: str) -> Environment:
    env = await Environment.from_tarball(env_tarball, str(tmp_path))
    yield env

    # Envs can be quite heavy, so let's make sure we're clearing them up once
    # the test finishes
    shutil.rmtree(tmp_path)


@pytest.fixture(autouse=True)
def logger(settings: Settings):
    return configure_logger(settings)


@pytest.fixture
def metrics_registry() -> MetricsRegistry:
    yield METRICS_REGISTRY

    unregister_metrics(METRICS_REGISTRY)


@pytest.fixture
def prometheus_registry(metrics_registry: MetricsRegistry) -> CollectorRegistry:
    """
    Fixture used to ensure the registry is cleaned on each run.
    Otherwise, `py-grpc-prometheus` will complain that metrics already exist.

    TODO: Open issue in `py-grpc-prometheus` to check whether a metric exists
    before creating it.
    For an example on how to do this, see `starlette_exporter`'s implementation

        https://github.com/stephenhillier/starlette_exporter/blob/947d4d631dd9a6a8c1071b45573c5562acba4834/starlette_exporter/middleware.py#L67
    """
    yield REGISTRY

    unregister_metrics(REGISTRY)

    # Clean metrics from `starlette_exporter` as well, as otherwise they won't
    # get re-created
    PrometheusMiddleware._metrics.clear()


@pytest.fixture
def event_loop():
    # By default use uvloop for tests
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sum_model_settings() -> ModelSettings:
    model_settings_path = os.path.join(TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME)
    return ModelSettings.parse_file(model_settings_path)


@pytest.fixture
def simple_model_settings() -> ModelSettings:
    model_settings_path = os.path.join(TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME)
    model_settings = ModelSettings.parse_file(model_settings_path)
    model_settings.name = "simple-model"
    model_settings.implementation = SimpleModel
    return model_settings


@pytest.fixture
def error_model_settings() -> ModelSettings:
    model_settings_path = os.path.join(TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME)
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
async def simple_model(
    model_registry: MultiModelRegistry, simple_model_settings: ModelSettings
) -> SimpleModel:
    await model_registry.load(simple_model_settings)
    return await model_registry.get_model(simple_model_settings.name)


@pytest.fixture
async def sum_model(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
) -> SumModel:
    return await model_registry.get_model(sum_model_settings.name)


@pytest.fixture
def text_model_settings() -> ModelSettings:
    # TODO: Enable parallel_workers once stream is supported
    return ModelSettings(
        name="text-model", implementation=TextModel, parallel_workers=0
    )


@pytest.fixture
async def text_model(
    model_registry: MultiModelRegistry, text_model_settings: ModelSettings
) -> TextModel:
    await model_registry.load(text_model_settings)
    return await model_registry.get_model(text_model_settings.name)


@pytest.fixture
def metadata_server_response() -> types.MetadataServerResponse:
    payload_path = os.path.join(TESTDATA_PATH, "metadata-server-response.json")
    return types.MetadataServerResponse.parse_file(payload_path)


@pytest.fixture
def metadata_model_response() -> types.MetadataModelResponse:
    payload_path = os.path.join(TESTDATA_PATH, "metadata-model-response.json")
    return types.MetadataModelResponse.parse_file(payload_path)


@pytest.fixture
def inference_request() -> types.InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return types.InferenceRequest.parse_file(payload_path)


@pytest.fixture
def inference_request_invalid_datatype() -> Dict[str, Any]:
    payload_path = os.path.join(
        TESTDATA_PATH, "inference-request-invalid-datatype.json"
    )
    with open(payload_path, "r") as payload_file:
        inference_request = json.load(payload_file)
    return inference_request


@pytest.fixture
def inference_response() -> types.InferenceResponse:
    payload_path = os.path.join(TESTDATA_PATH, "inference-response.json")
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
def data_plane(
    settings: Settings,
    model_registry: MultiModelRegistry,
    prometheus_registry: CollectorRegistry,
) -> DataPlane:
    return DataPlane(settings=settings, model_registry=model_registry)


@pytest.fixture
def model_repository_handlers(
    model_repository: ModelRepository, model_registry: MultiModelRegistry
) -> ModelRepositoryHandlers:
    return ModelRepositoryHandlers(
        repository=model_repository, model_registry=model_registry
    )


@pytest.fixture
def model_folder(tmp_path: str) -> str:
    to_copy = [DEFAULT_MODEL_SETTINGS_FILENAME]

    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = os.path.join(tmp_path, file_name)
        shutil.copyfile(src, dst)

    return str(tmp_path)


@pytest.fixture
def model_repository(model_folder: str) -> ModelRepository:
    return SchemalessModelRepository(model_folder)


@pytest.fixture
def repository_index_request() -> types.RepositoryIndexRequest:
    return types.RepositoryIndexRequest(ready=None)


@pytest.fixture
def repository_index_response(sum_model_settings) -> types.RepositoryIndexResponse:
    return types.RepositoryIndexResponse(
        root=[
            types.RepositoryIndexResponseItem(
                name=sum_model_settings.name,
                version=sum_model_settings.parameters.version,
                state=types.State.READY,
                reason="",
            ),
        ]
    )


@pytest.fixture
def _mlserver_settings(settings: Settings, tmp_path: str):
    """
    This is an indirect fixture used to tweak the standard settings ONLY when
    the `mlserver` fixture is used.
    You shouldn't need to use this fixture directly.
    """
    http_port, grpc_port, metrics_port = get_available_ports(3)
    settings.http_port = http_port
    settings.grpc_port = grpc_port
    settings.metrics_port = metrics_port
    settings.metrics_dir = str(tmp_path)

    return settings


@pytest.fixture
async def mlserver(
    _mlserver_settings: Settings,
    sum_model_settings: ModelSettings,
    prometheus_registry: CollectorRegistry,
):
    server = MLServer(_mlserver_settings)

    # Start server without blocking, and cancel afterwards
    server_task = asyncio.create_task(server.start())

    # Load sample model
    await server._model_registry.load(sum_model_settings)

    yield server

    await server.stop()
    await server_task

    pattern = os.path.join(_mlserver_settings.metrics_dir, "*.db")
    prom_files = glob.glob(pattern)
    assert not prom_files


@pytest.fixture
async def rest_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    client = RESTClient(http_server)

    yield client

    await client.close()


@pytest.fixture
async def inference_pool_registry(
    settings: Settings, prometheus_registry: CollectorRegistry
) -> InferencePoolRegistry:
    registry = InferencePoolRegistry(settings)
    yield registry

    await registry.close()


@pytest.fixture
def datatype_error_message():
    error_message = (
        "Input should be"
        " 'BOOL', 'UINT8', 'UINT16', 'UINT32',"
        " 'UINT64', 'INT8', 'INT16', 'INT32', 'INT64',"
        " 'FP16', 'FP32', 'FP64' or 'BYTES'"
    )
    return error_message
