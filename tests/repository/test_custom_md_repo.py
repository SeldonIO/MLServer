from mlserver.settings import Settings

from ..utils import RESTClient


async def test_custom_model_repo_by_settings(
    rest_client: RESTClient,
    settings: Settings,
):
    await rest_client.wait_until_model_ready("sum-model")

    result = await rest_client.list_models()

    assert len(result) == 1
