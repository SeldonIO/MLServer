import pytest
import os
import shutil

from ..conftest import TESTDATA_PATH


@pytest.fixture
def model_folder(tmp_path):
    to_copy = ["settings.json", "model-settings.json"]

    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = tmp_path.joinpath(file_name)
        shutil.copyfile(src, dst)

    return tmp_path


@pytest.fixture
def model_folder_with_reqs(model_folder):
    reqs_txt = "requirements.txt"
    src = os.path.join(TESTDATA_PATH, reqs_txt)
    dst = model_folder.join_path(reqs_txt)
    shutil.copyfile(src, dst)

    return model_folder
