import pytest
import shutil
import os


from ..conftest import TESTDATA_PATH


@pytest.fixture
def env_tarball(tmp_path: str) -> str:
    src = os.path.join(TESTDATA_PATH, "environment.tar.gz")
    dst = os.path.join(tmp_path, "environment.tar.gz")
    shutil.copyfile(src, dst)
    return dst
