import os
import sys
import pytest
import json

from mlserver.settings import CORSSettings, Settings, ModelSettings, ModelParameters
from mlserver.repository import DEFAULT_MODEL_SETTINGS_FILENAME

from .conftest import TESTDATA_PATH, TESTS_PATH


def test_settings_from_env(monkeypatch):
    http_port = 5000
    monkeypatch.setenv("mlserver_http_port", str(http_port))

    settings = Settings()

    assert settings.http_port == http_port


def test_settings_from_env_file(monkeypatch):
    env_file = f"{TESTDATA_PATH}/.test.env"

    settings = Settings(_env_file=env_file)
    cors_settings = CORSSettings(_env_file=env_file)
    model_settings = ModelSettings(_env_file=env_file)
    model_settings.parameters = ModelParameters(_env_file=env_file)

    assert settings.http_port == 9999
    assert settings.debug is True

    assert cors_settings.allow_origin_regex == ".*"
    assert cors_settings.max_age == 999

    assert model_settings.name == "dummy-name"
    assert model_settings.parameters.uri == "dummy-uri"


def test_model_settings_from_env(monkeypatch):
    model_name = "foo-model"
    model_version = "v0.1.0"
    model_uri = "/mnt/models/my-model"

    monkeypatch.setenv("mlserver_model_name", model_name)
    monkeypatch.setenv("mlserver_model_version", model_version)
    monkeypatch.setenv("mlserver_model_uri", model_uri)
    monkeypatch.setenv("mlserver_model_implementation", "mlserver.MLModel")

    model_settings = ModelSettings()
    model_settings.parameters = ModelParameters()

    assert model_settings.name == model_name
    assert model_settings.parameters.version == model_version
    assert model_settings.parameters.uri == model_uri


@pytest.mark.parametrize(
    "obj",
    [
        ({"name": "foo", "implementation": "tests.fixtures.SumModel"}),
        (
            {
                "_source": os.path.join(TESTS_PATH, DEFAULT_MODEL_SETTINGS_FILENAME),
                "name": "foo",
                "implementation": "fixtures.SumModel",
            }
        ),
    ],
)
def test_model_settings_model_validate(obj: dict):
    pre_sys_path = sys.path[:]
    model_settings = ModelSettings.model_validate(obj)
    post_sys_path = sys.path[:]

    assert pre_sys_path == post_sys_path
    assert model_settings.implementation.__name__ == "SumModel"


def test_model_settings_serialisation():
    # Module may have been reloaded in a diff test, so let's re-import it
    from .fixtures import SumModel

    expected = "tests.fixtures.SumModel"
    model_settings = ModelSettings(name="foo", implementation=SumModel)

    assert model_settings.implementation == SumModel
    assert model_settings.implementation_ == expected

    # Dump `by_alias` to ensure that our alias overrides [1] are used
    # [2][3].
    #
    # > Whether to serialize using field aliases. [2][3]
    #
    # [1] https://github.com/jesse-c/MLServer/blob/4ac2da1d0dd7aa4b3796c047013b841fffa60e58/mlserver/settings.py#L373-L376  # noqa: E501
    # [2]  https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump  # noqa: E501
    # [3]  https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump_json  # noqa: E501

    as_dict = model_settings.model_dump(by_alias=True)
    as_dict["implementation"] == expected

    as_json = model_settings.model_dump_json(by_alias=True)
    as_dict = json.loads(as_json)
    as_dict["implementation"] == expected


def test_model_settings_streaming(caplog):
    with pytest.raises(ValueError) as err:
        _ = Settings(parallel_workers=2, streaming_enabled=True)

    assert "Streaming is not supported with `parallel_workers' > 0" in str(err.value)
