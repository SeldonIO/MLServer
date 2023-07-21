import pytest

from typing import Optional

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.context import model_context, MODEL_NAME_VAR, MODEL_VERSION_VAR
from .fixtures import SumModel


@pytest.mark.parametrize(
    "name, version, expected_version",
    [
        (
            "foo",
            "v1.0",
            "v1.0",
        ),
        (
            "foo",
            "",
            "",
        ),
        ("foo", None, ""),
    ],
)
def test_model_context(name: str, version: Optional[str], expected_version: str):
    model_settings = ModelSettings(
        name=name, implementation=SumModel, parameters=ModelParameters(version=version)
    )

    with pytest.raises(LookupError):
        _ = MODEL_NAME_VAR.get()

    with pytest.raises(LookupError):
        _ = MODEL_VERSION_VAR.get()

    with model_context(model_settings):
        var_name = MODEL_NAME_VAR.get()
        var_version = MODEL_VERSION_VAR.get()
        assert var_name == name
        assert var_version == expected_version

    with pytest.raises(LookupError):
        _ = MODEL_NAME_VAR.get()

    with pytest.raises(LookupError):
        _ = MODEL_VERSION_VAR.get()
