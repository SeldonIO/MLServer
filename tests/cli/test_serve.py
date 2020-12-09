import os

from mlserver.cli.serve import DEFAULT_SETTINGS_FILENAME, load_settings
from mlserver.settings import Settings, ModelSettings


async def test_load_models(sum_model_settings: ModelSettings, model_folder: str):
    _, models = await load_settings(model_folder)

    assert len(models) == 1
    assert models[0].name == sum_model_settings.name
    assert models[0].version == sum_model_settings.parameters.version  # type: ignore


async def test_disable_load_models(settings: Settings, model_folder: str):
    settings.load_models_at_startup = False

    settings_path = os.path.join(model_folder, DEFAULT_SETTINGS_FILENAME)
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings.json())

    _, models = await load_settings(model_folder)

    assert len(models) == 0
