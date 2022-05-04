import os
import pytest
import asyncio
import platform

from mlserver.cli.serve import (
    DEFAULT_SETTINGS_FILENAME,
    load_settings,
    install_configured_event_loop,
)
from mlserver.settings import Settings, ModelSettings


async def test_load_models(sum_model_settings: ModelSettings, model_folder: str):
    _, models_settings = await load_settings(model_folder)

    assert len(models_settings) == 1

    model_settings = models_settings[0]
    parameters = models_settings[0].parameters
    assert model_settings.name == sum_model_settings.name
    assert parameters.version == sum_model_settings.parameters.version  # type: ignore


async def test_disable_load_models(settings: Settings, model_folder: str):
    settings.load_models_at_startup = False

    settings_path = os.path.join(model_folder, DEFAULT_SETTINGS_FILENAME)
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings.json())

    _, models_settings = await load_settings(model_folder)

    assert len(models_settings) == 0


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.fixture
def uvloop_settings(settings: Settings) -> Settings:
    settings.event_loop = "uvloop"
    return settings


@pytest.fixture
def asyncio_settings(settings: Settings) -> Settings:
    settings.event_loop = "asyncio"
    return settings


@pytest.fixture
def auto_settings(settings: Settings) -> Settings:
    settings.event_loop = "auto"
    return settings


def _check_uvloop_availability():
    avail = True
    try:
        import uvloop  # noqa: F401
    except ImportError:  # pragma: no cover
        avail = False
    return avail


def test_asyncio_install(asyncio_settings: Settings):
    install_configured_event_loop(asyncio_settings)
    policy = asyncio.get_event_loop_policy()
    if platform.system() == "Windows":
        assert isinstance(policy, asyncio.WindowsProactorEventLoopPolicy)
    else:
        assert isinstance(policy, asyncio.DefaultEventLoopPolicy)


def test_uvloop_install(uvloop_settings: Settings):
    uvloop_available = _check_uvloop_availability()

    if uvloop_available:
        install_configured_event_loop(uvloop_settings)
        policy = asyncio.get_event_loop_policy()
        assert type(policy).__module__.startswith("uvloop")
    else:
        with pytest.raises(ImportError):
            assert install_configured_event_loop(uvloop_settings)


def test_auto_install(auto_settings: Settings):
    uvloop_available = _check_uvloop_availability()
    install_configured_event_loop(auto_settings)
    policy = asyncio.get_event_loop_policy()

    if uvloop_available:
        assert type(policy).__module__.startswith("uvloop")
    else:
        if platform.system() == "Windows":
            assert isinstance(policy, asyncio.WindowsProactorEventLoopPolicy)
        elif platform.python_implementation() != "CPython":
            assert isinstance(policy, asyncio.DefaultEventLoopPolicy)
