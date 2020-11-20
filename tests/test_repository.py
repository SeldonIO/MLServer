import os

from mlserver.repository import ModelRepository, DEFAULT_MODEL_SETTINGS_FILENAME
from mlserver.settings import ModelSettings, ENV_PREFIX_MODEL_SETTINGS

from .helpers import get_import_path


def test_list(sum_model_settings: ModelSettings, model_repository: ModelRepository):
    settings_list = model_repository.list()

    assert len(settings_list) == 1
    assert settings_list[0].name == sum_model_settings.name
    assert settings_list[0].parameters.version == sum_model_settings.parameters.version
    assert settings_list[0].parameters.uri == str(model_repository._root)


def test_list_multi_model(multi_model_folder: str):
    multi_model_loader = ModelRepository(multi_model_folder)

    settings_list = multi_model_loader.list()
    settings_list.sort(key=lambda ms: ms.parameters.version)

    assert len(settings_list) == 5
    for idx, model_settings in enumerate(settings_list):
        # Models get read in reverse
        assert model_settings.parameters.version == f"v{idx}"


def test_list_fallback(
    monkeypatch,
    model_folder: str,
    sum_model_settings: ModelSettings,
    model_repository: ModelRepository,
):
    monkeypatch.setenv(f"{ENV_PREFIX_MODEL_SETTINGS}NAME", sum_model_settings.name)
    monkeypatch.setenv(
        f"{ENV_PREFIX_MODEL_SETTINGS}VERSION", sum_model_settings.parameters.version
    )
    monkeypatch.setenv(
        f"{ENV_PREFIX_MODEL_SETTINGS}IMPLEMENTATION",
        get_import_path(sum_model_settings.implementation),  # type: ignore
    )

    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    os.remove(model_settings_path)

    all_settings = model_repository.list()

    assert len(all_settings) == 1
    assert all_settings[0].name == sum_model_settings.name
    assert all_settings[0].parameters.version == sum_model_settings.parameters.version
