import pytest
from ..utils import file_path, file_bytescontent


@pytest.fixture
def audio_filepath():
    return file_path("audio.mp3")


@pytest.fixture
def audio_filebytes():
    return file_bytescontent("audio.mp3")
