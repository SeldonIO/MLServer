import pytest

from typing import Optional
from unittest.mock import patch

from mlserver.utils import get_model_uri
from mlserver.settings import ModelSettings, ModelParameters


@pytest.mark.parametrize(
    "uri, source, expected",
    [
        ("my-model.bin", None, "my-model.bin"),
        (
            "my-model.bin",
            "./my-model-folder/model-settings.json",
            "my-model-folder/my-model.bin",
        ),
        (
            "my-model.bin",
            "./my-model-folder/../model-settings.json",
            "my-model.bin",
        ),
        (
            "/an/absolute/path/my-model.bin",
            "/mnt/models/model-settings.json",
            "/an/absolute/path/my-model.bin",
        ),
    ],
)
@patch("os.path.isfile", return_value=True)
async def test_get_model_uri(
    mock_isfile, uri: str, source: Optional[str], expected: str
):
    model_settings = ModelSettings(parameters=ModelParameters(uri=uri))
    model_settings._source = source
    model_uri = await get_model_uri(model_settings)

    assert model_uri == expected
