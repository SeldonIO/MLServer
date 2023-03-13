import os
import pytest

from mlserver.settings import Settings

from ..conftest import TESTDATA_PATH


@pytest.fixture
def settings() -> Settings:
    settings_path = os.path.join(TESTDATA_PATH, "settings-custom-md-repo.json")
    return Settings.parse_file(settings_path)
