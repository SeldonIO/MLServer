import os
import json
import pytest
import shutil

from mlserver.repository.repository import (
    ModelRepository,
    DEFAULT_MODEL_SETTINGS_FILENAME,
)
from mlserver.repository.load import load_model_settings
from mlserver.settings import ModelSettings

from ..conftest import TESTDATA_PATH
from .utils import get_import_path


@pytest.fixture
def custom_module_settings_path(
    sum_model_settings: ModelSettings, tmp_path: str
) -> str:
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

    return model_settings_path


async def test_name_fallback(
    sum_model_settings: ModelSettings,
    model_folder: str,
):
    # Create empty model-settings.json file
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as model_settings_file:
        d = sum_model_settings.dict()
        del d["name"]
        d["implementation"] = get_import_path(d["implementation"])
        json.dump(d, model_settings_file)

    model_settings = load_model_settings(model_settings_path)
    assert model_settings.name == os.path.basename(model_folder)


async def test_list_custom_module(
    custom_module_settings_path: str, sum_model_settings: ModelSettings
):
    model_settings = load_model_settings(custom_module_settings_path)

    assert model_settings.name == sum_model_settings.name
    assert get_import_path(model_settings.implementation) == "models.SumModel"
