from mlserver.cli.serve import (
    load_settings,
)
from mlserver.settings import (
    ModelSettings,
)


def test_load_models(sum_model_settings: ModelSettings, model_folder: str):
    _, models = load_settings(model_folder)

    assert len(models) == 1
    assert models[0].name == sum_model_settings.name
    assert models[0].version == sum_model_settings.parameters.version
