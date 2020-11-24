from mlserver.cli.serve import (
    load_settings,
)
from mlserver.settings import (
    ModelSettings,
)


async def test_load_models(sum_model_settings: ModelSettings, model_folder: str):
    _, models = await load_settings(model_folder)

    assert len(models) == 1
    assert models[0].name == sum_model_settings.name
    assert models[0].version == sum_model_settings.parameters.version  # type: ignore
