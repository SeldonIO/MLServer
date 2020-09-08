from mlserver.cli.serve import read_folder
from mlserver.settings import ModelSettings


def test_read_folder(sum_model_settings: ModelSettings, model_folder: str):
    _, models = read_folder(model_folder)

    assert len(models) == 1
    assert models[0].name == sum_model_settings.name
    assert models[0].version == sum_model_settings.version
