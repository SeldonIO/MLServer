from mlserver.cli.serve import init_mlserver
from mlserver.settings import ModelSettings


def test_init_mlserver(sum_model_settings: ModelSettings, model_folder: str):
    server = init_mlserver(model_folder)

    model = server._model_repository.get_model(
        name=sum_model_settings.name, version=sum_model_settings.version
    )
    assert model is not None
