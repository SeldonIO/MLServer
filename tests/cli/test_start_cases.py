import os
import shutil
import json

from mlserver.settings import ModelSettings, Settings
from mlserver.cli.serve import DEFAULT_SETTINGS_FILENAME
from mlserver.repository import DEFAULT_MODEL_SETTINGS_FILENAME

from ..conftest import TESTDATA_PATH


def _init_model_folder(tmp_path: str, settings: Settings):
    # Write settings.json with free ports
    settings_path = os.path.join(tmp_path, DEFAULT_SETTINGS_FILENAME)
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings.json())

    # Copy models.py module
    src_path = os.path.join(TESTDATA_PATH, "models.py")
    dst_path = os.path.join(tmp_path, "models.py")
    shutil.copy(src_path, dst_path)


def case_sum_model(tmp_path: str, settings: Settings) -> str:
    _init_model_folder(tmp_path, settings)

    # Copy SumModel's model-settings.json
    sum_model_folder = os.path.join(tmp_path, "sum-model")
    os.makedirs(sum_model_folder)
    old_path = os.path.join(TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME)
    new_path = os.path.join(sum_model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    shutil.copy(old_path, new_path)

    return tmp_path


def case_slow_model(
    tmp_path: str, settings: Settings, sum_model_settings: ModelSettings
) -> str:
    _init_model_folder(tmp_path, settings)

    # Write SlowModel's model-settings.json
    slow_model_folder = os.path.join(tmp_path, "sum-model")
    os.makedirs(slow_model_folder)
    slow_model_settings_path = os.path.join(
        slow_model_folder, DEFAULT_MODEL_SETTINGS_FILENAME
    )
    with open(slow_model_settings_path, "w") as slow_model_file:
        as_dict = sum_model_settings.dict()
        as_dict["implementation"] = "models.SlowModel"
        slow_model_file.write(json.dumps(as_dict))

    return tmp_path
