import pytest
import os
import shutil
import json

from mlserver.cli.serve import DEFAULT_MODEL_SETTINGS_FILENAME

from ..conftest import TESTDATA_PATH

from .helpers import get_import_path


@pytest.fixture
def model_folder(tmp_path):
    to_copy = ["settings.json", "model-settings.json"]

    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = tmp_path.joinpath(file_name)
        shutil.copyfile(src, dst)

    return tmp_path


@pytest.fixture
def multi_model_folder(model_folder, sum_model_settings):
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
def model_folder_with_reqs(model_folder):
    reqs_txt = model_folder / "requirements.txt"
    reqs_txt.write_text("numpy==1.18.5")

    return model_folder
