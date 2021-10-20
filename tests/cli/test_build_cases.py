import os
import shutil

from typing import List

from ..conftest import TESTDATA_PATH


def _copy_test_files(model_folder: str, to_copy: List[str]) -> str:
    to_copy = ["models.py", "environment.yml"]
    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = os.path.join(model_folder, file_name)
        shutil.copyfile(src, dst)

    return model_folder


def case_no_custom_env(model_folder: str) -> str:
    """
    Custom model with no custom environment required.
    """
    to_copy = ["models.py", "environment.yml"]
    return _copy_test_files(model_folder, to_copy=to_copy)


def case_environment_yml(model_folder: str) -> str:
    """
    Custom model with environment provided through an environment.yml file.
    """
    to_copy = ["env_models.py", "environment.yml"]
    return _copy_test_files(model_folder, to_copy=to_copy)


def case_requirements_txt_path(model_folder: str) -> str:
    """
    Custom model with environment provided through a requirements.txt file.
    """
    to_copy = ["env_models.py", "requirements.txt"]
    return _copy_test_files(model_folder, to_copy=to_copy)
