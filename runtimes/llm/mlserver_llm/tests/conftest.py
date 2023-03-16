import os
from pathlib import Path

import pytest

from mlserver.settings import Settings

TESTS_PATH = Path(os.path.dirname(__file__))


@pytest.fixture
def settings() -> Settings:
    return Settings(debug=True, host="127.0.0.1")
