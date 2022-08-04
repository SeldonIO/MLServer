from mlserver.settings import CORSSettings, Settings, ModelSettings, ModelParameters
from .conftest import TESTDATA_PATH


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
