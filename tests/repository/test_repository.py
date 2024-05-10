import os
import pytest

from mlserver.repository import (
    ModelRepository,
    SchemalessModelRepository,
    DEFAULT_MODEL_SETTINGS_FILENAME,
)
from mlserver.settings import ModelSettings, ENV_PREFIX_MODEL_SETTINGS


@pytest.fixture
def multi_model_folder(model_folder: str, sum_model_settings: ModelSettings) -> str:
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
            settings_json = sum_model_settings.model_dump_json(by_alias=True)
            f.write(settings_json)

    return model_folder


async def test_list(
    sum_model_settings: ModelSettings, model_repository: ModelRepository
):
    settings_list = await model_repository.list()

    assert len(settings_list) == 1

    loaded_model_settings = settings_list[0]
    assert loaded_model_settings.name == sum_model_settings.name
    assert (
        loaded_model_settings.parameters.version  # type: ignore
        == sum_model_settings.parameters.version  # type: ignore
    )
    assert loaded_model_settings.parameters.uri == str(  # type: ignore
        model_repository._root
    )
    assert loaded_model_settings._source == os.path.join(
        model_repository._root, DEFAULT_MODEL_SETTINGS_FILENAME
    )


async def test_list_multi_model(multi_model_folder: str):
    multi_model_repository = SchemalessModelRepository(multi_model_folder)

    settings_list = await multi_model_repository.list()
    settings_list.sort(key=lambda ms: ms.parameters.version)  # type: ignore

    assert len(settings_list) == 5
    for idx, model_settings in enumerate(settings_list):
        model_settings_path = os.path.join(
            multi_model_folder,
            model_settings.name,
            model_settings.parameters.version,
            DEFAULT_MODEL_SETTINGS_FILENAME,
        )

        assert model_settings.parameters.version == f"v{idx}"  # type: ignore
        assert model_settings._source == model_settings_path


async def test_list_fallback(
    monkeypatch,
    model_folder: str,
    sum_model_settings: ModelSettings,
    model_repository: ModelRepository,
):
    monkeypatch.setenv(f"{ENV_PREFIX_MODEL_SETTINGS}NAME", sum_model_settings.name)
    monkeypatch.setenv(
        f"{ENV_PREFIX_MODEL_SETTINGS}VERSION",
        sum_model_settings.parameters.version,  # type: ignore
    )
    monkeypatch.setenv(
        f"{ENV_PREFIX_MODEL_SETTINGS}IMPLEMENTATION",
        sum_model_settings.implementation_,  # type: ignore
    )

    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    os.remove(model_settings_path)

    all_settings = await model_repository.list()

    assert len(all_settings) == 1

    default_model_settings = all_settings[0]
    assert default_model_settings.name == sum_model_settings.name
    assert (
        default_model_settings.parameters.version  # type: ignore
        == sum_model_settings.parameters.version  # type: ignore
    )
    assert default_model_settings._source is None


async def test_find(
    model_repository: ModelRepository, sum_model_settings: ModelSettings
):
    found_model_settings = await model_repository.find(sum_model_settings.name)

    assert len(found_model_settings) == 1
    assert found_model_settings[0].name == sum_model_settings.name
