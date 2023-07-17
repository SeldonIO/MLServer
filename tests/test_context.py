import pytest

from typing import Optional

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.context import model_context, model_name_var, model_version_var
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
        _ = model_name_var.get()

    with pytest.raises(LookupError):
        _ = model_version_var.get()

    with model_context(model_settings):
        var_name = model_name_var.get()
        var_version = model_version_var.get()
        assert var_name == name
        assert var_version == expected_version

    with pytest.raises(LookupError):
        _ = model_name_var.get()

    with pytest.raises(LookupError):
        _ = model_version_var.get()
