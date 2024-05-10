import os
import shutil
import json

from mlserver.settings import ModelSettings, Settings
from mlserver.cli.serve import DEFAULT_SETTINGS_FILENAME
from mlserver.repository import DEFAULT_MODEL_SETTINGS_FILENAME

from ..conftest import TESTS_PATH, TESTDATA_PATH


def _init_mlserver_folder(tmp_path: str, settings: Settings):
    # Write settings.json with free ports
    settings_path = os.path.join(tmp_path, DEFAULT_SETTINGS_FILENAME)
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings.model_dump_json())

    # Copy fixtures.py module
    src_path = os.path.join(TESTS_PATH, "fixtures.py")
    dst_path = os.path.join(tmp_path, "fixtures.py")
    shutil.copy(src_path, dst_path)

    # Write SlowModel's model-settings.json
    model_folder = os.path.join(tmp_path, "slow-model")
    os.makedirs(model_folder)
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as model_settings_file:
        model_settings = {"name": "slow-model", "implementation": "fixtures.SlowModel"}
        model_settings_file.write(json.dumps(model_settings))


def case_sum_model(
    tmp_path: str, settings: Settings, sum_model_settings: ModelSettings
) -> str:
    _init_mlserver_folder(tmp_path, settings)

    # Copy SumModel's model-settings.json
    model_folder = os.path.join(tmp_path, sum_model_settings.name)
    os.makedirs(model_folder)
    old_path = os.path.join(TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME)
    new_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    shutil.copy(old_path, new_path)

    return tmp_path


def case_custom_module(
    tmp_path: str, settings: Settings, sum_model_settings: ModelSettings
) -> str:
    _init_mlserver_folder(tmp_path, settings)

    model_folder = os.path.join(tmp_path, sum_model_settings.name)
    os.makedirs(model_folder)

    # Copy fixtures.py module
    src_path = os.path.join(TESTS_PATH, "fixtures.py")
    dst_path = os.path.join(model_folder, "custom.py")
    shutil.copy(src_path, dst_path)

    # Write model settings pointing to local module
    model_settings_path = os.path.join(model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    with open(model_settings_path, "w") as model_settings_file:
        as_dict = sum_model_settings.model_dump()
        as_dict["implementation"] = "custom.SumModel"
        model_settings_file.write(json.dumps(as_dict))

    return tmp_path
