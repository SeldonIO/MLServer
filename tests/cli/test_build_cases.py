import os
import shutil
import json

from typing import List

from ..conftest import TESTS_PATH, TESTDATA_PATH
from ..utils import _render_env_yml


def _copy_test_files(
    model_folder: str, model_settings: dict, to_copy: List[str]
) -> str:
    model_settings_path = os.path.join(model_folder, "model-settings.json")
    with open(model_settings_path, "w") as model_settings_file:
        model_settings_file.write(json.dumps(model_settings))

    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = os.path.join(model_folder, file_name)
        shutil.copyfile(src, dst)

    return model_folder


def case_no_custom_env(tmp_path: str) -> str:
    """
    Custom model with no custom environment required.
    """
    src = os.path.join(TESTS_PATH, "fixtures.py")
    dst = os.path.join(tmp_path, "fixtures.py")
    shutil.copyfile(src, dst)

    model_settings = {"name": "no_custom_env", "implementation": "fixtures.SumModel"}
    return _copy_test_files(tmp_path, model_settings, to_copy=[])


def case_environment_yml(tmp_path: str) -> str:
    """
    Custom model with environment provided through an environment.yml file.
    """
    to_copy = ["env_models.py"]
    _render_env_yml(
        os.path.join(TESTDATA_PATH, "environment.yml"),
        os.path.join(tmp_path, "environment.yml"),
    )
    model_settings = {
        "name": "environment-yml",
        "implementation": "env_models.DummySKLearnModel",
    }
    return _copy_test_files(tmp_path, model_settings, to_copy=to_copy)


def case_requirements_txt_path(tmp_path: str) -> str:
    """
    Custom model with environment provided through a requirements.txt file.
    """
    to_copy = ["env_models.py", "requirements.txt"]
    model_settings = {
        "name": "requirements-txt",
        "implementation": "env_models.DummySKLearnModel",
    }
    return _copy_test_files(tmp_path, model_settings, to_copy=to_copy)
