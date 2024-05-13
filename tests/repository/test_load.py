import os
import json
import pytest
import shutil
import sys

from mlserver.model import MLModel
from mlserver.repository.repository import DEFAULT_MODEL_SETTINGS_FILENAME
from mlserver.repository.load import load_model_settings
from mlserver.settings import ModelSettings

from ..conftest import TESTS_PATH


@pytest.fixture
def custom_module_settings_path(
    sum_model_settings: ModelSettings, tmp_path: str
) -> str:
    # Copy fixtures.py, which acts as custom module
    src = os.path.join(TESTS_PATH, "fixtures.py")
    dst = os.path.join(tmp_path, "fixtures.py")
    shutil.copyfile(src, dst)

    # Add modified settings, pointing to local module
    model_settings_path = os.path.join(tmp_path, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as f:
        settings_dict = sum_model_settings.model_dump()
        # Point to local module
        settings_dict["implementation"] = "fixtures.SumModel"
        f.write(json.dumps(settings_dict))

    return model_settings_path


async def test_load_model_settings(
    sum_model_settings: MLModel, model_folder: ModelSettings
):
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    model_settings = load_model_settings(model_settings_path)

    assert model_settings.name == sum_model_settings.name
    assert (
        model_settings.parameters.version  # type: ignore
        == sum_model_settings.parameters.version  # type: ignore
    )
    assert model_settings._source == model_settings_path


async def test_name_fallback(
    sum_model_settings: ModelSettings,
    model_folder: str,  # This is effectively the Pytest-provided `tmp_path` fixture
):
    # Overwrite `model-settings.json` file to be missing the `name` field
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as model_settings_file:
        d = sum_model_settings.model_dump(by_alias=True)

        # Remove the `name` field from the JSON representation
        del d["name"]

        # Overwrite the model settings in the temporary path
        json.dump(d, model_settings_file)

    model_settings = load_model_settings(model_settings_path)

    # Check that it picked up the model name from the
    # `model-settings.json`'s containing folder.
    assert model_settings.name == os.path.basename(model_folder)


async def test_load_custom_module(
    custom_module_settings_path: str, sum_model_settings: ModelSettings
):
    pre_sys_path = sys.path[:]
    model_settings = load_model_settings(custom_module_settings_path)
    post_sys_path = sys.path[:]

    assert pre_sys_path == post_sys_path
    assert model_settings.name == sum_model_settings.name
    assert model_settings.implementation_ == "fixtures.SumModel"
