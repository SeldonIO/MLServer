import os
import json
import pytest
import shutil

from mlserver.repository import ModelRepository, DEFAULT_MODEL_SETTINGS_FILENAME
from mlserver.settings import ModelSettings, ENV_PREFIX_MODEL_SETTINGS

from .helpers import get_import_path
from .conftest import TESTDATA_PATH


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
            settings_dict = sum_model_settings.dict()
            settings_dict["implementation"] = get_import_path(
                sum_model_settings.implementation
            )
            f.write(json.dumps(settings_dict))

    return model_folder


@pytest.fixture
def custom_module_folder(model_settings: ModelSettings, tmp_path: str) -> str:
    # Copy models.py, which acts as custom module
    src = os.path.join(TESTDATA_PATH, "models.py")
    dst = os.path.join(tmp_path, "models.py")
    shutil.copyfile(src, dst)

    # Add modified settings, pointing to local module
    model_settings_path = os.path.join(tmp_path, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as f:
        settings_dict = sum_model_settings.dict()
        # Point to local module
        settings_dict["implementation"] = "models.SumModel"
        f.write(json.dumps(settings_dict))

    return str(tmp_path)


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


#  async def test_list_custom_module(
#  custom_module_folder: str, sum_model_settings: ModelSettings
#  ):
#  multi_model_repository = ModelRepository(custom_module_folder)

#  settings_list = await multi_model_repository.list()

#  assert len(settings_list) == 1
#  model_settings = settings_list[0]
#  assert model_settings.name == sum_model_settings.name
#  assert get_import_path(model_settings.implementation) == "models.SumModel"


async def test_list_multi_model(multi_model_folder: str):
    multi_model_repository = ModelRepository(multi_model_folder)

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
        get_import_path(sum_model_settings.implementation),  # type: ignore
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


async def test_name_fallback(
    sum_model_settings: ModelSettings,
    model_folder: str,
    model_repository: ModelRepository,
):
    # Create empty model-settings.json file
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as model_settings_file:
        d = sum_model_settings.dict()
        del d["name"]
        d["implementation"] = get_import_path(d["implementation"])
        json.dump(d, model_settings_file)

    model_settings = model_repository._load_model_settings(model_settings_path)
    assert model_settings.name == os.path.basename(model_folder)


async def test_find(
    model_repository: ModelRepository, sum_model_settings: ModelSettings
):
    found_model_settings = await model_repository.find(sum_model_settings.name)

    assert len(found_model_settings) == 1
    assert found_model_settings[0].name == sum_model_settings.name
