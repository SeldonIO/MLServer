import os

from mlserver.cli.serve import load_settings, DEFAULT_SETTINGS_FILENAME
from mlserver.settings import ModelSettings, ENV_PREFIX_SETTINGS


def test_load_settings(sum_model_settings: ModelSettings, model_folder: str):
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
