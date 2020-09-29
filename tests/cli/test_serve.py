import os

from mlserver.cli.serve import (
    load_settings,
    DEFAULT_MODEL_SETTINGS_FILENAME,
    DEFAULT_SETTINGS_FILENAME,
)
from mlserver.settings import (
    ModelSettings,
    ENV_PREFIX_MODEL_SETTINGS,
    ENV_PREFIX_SETTINGS,
)

from .helpers import get_import_path


def test_load_model_settings(sum_model_settings: ModelSettings, model_folder: str):
    _, models = load_settings(model_folder)

    assert len(models) == 1
    assert models[0].name == sum_model_settings.name
    assert models[0].version == sum_model_settings.version


def test_load_settings_multi_model(multi_model_folder: str):
    _, models = load_settings(multi_model_folder)
    models.sort(key=lambda m: m.version)

    assert len(models) == 5
    for idx, model in enumerate(models):
        # Models get read in reverse
        assert model.version == f"v{idx}"


def test_load_model_settings_fallback(
    monkeypatch, sum_model_settings: ModelSettings, model_folder: str
):
    monkeypatch.setenv(f"{ENV_PREFIX_MODEL_SETTINGS}NAME", sum_model_settings.name)
    monkeypatch.setenv(
        f"{ENV_PREFIX_MODEL_SETTINGS}VERSION", sum_model_settings.version
    )
    monkeypatch.setenv(
        f"{ENV_PREFIX_MODEL_SETTINGS}IMPLEMENTATION",
        get_import_path(sum_model_settings.implementation),
    )

    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    os.remove(model_settings_path)

    _, models = load_settings(model_folder)

    assert len(models) == 1
    assert models[0].name == sum_model_settings.name
    assert models[0].version == sum_model_settings.version


def test_load_settings_fallback(
    monkeypatch, sum_model_settings: ModelSettings, model_folder: str
):
    http_port = 5000
    monkeypatch.setenv(f"{ENV_PREFIX_SETTINGS}HTTP_PORT", str(http_port))

    settings_path = os.path.join(model_folder, DEFAULT_SETTINGS_FILENAME)
    os.remove(settings_path)

    settings, models = load_settings(model_folder)

    assert settings.http_port == http_port
    assert models[0].name == sum_model_settings.name
