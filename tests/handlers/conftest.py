import pytest
import os

from mlserver.settings import Settings
from mlserver.handlers import DataPlane
from mlserver.handlers.custom import CustomHandler
from mlserver.registry import MultiModelRegistry
from prometheus_client.registry import CollectorRegistry

from ..fixtures import SumModel
from ..conftest import TESTDATA_PATH


@pytest.fixture
def custom_handler(sum_model: SumModel) -> CustomHandler:
    return CustomHandler(rest_path="/my-custom-endpoint")


@pytest.fixture
def cached_settings() -> Settings:
    settings_path = os.path.join(TESTDATA_PATH, "settings-cache.json")
    return Settings.parse_file(settings_path)


@pytest.fixture
def cached_data_plane(
    cached_settings: Settings,
    model_registry: MultiModelRegistry,
    prometheus_registry: CollectorRegistry,
) -> DataPlane:
    return DataPlane(settings=cached_settings, model_registry=model_registry)
