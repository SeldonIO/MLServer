from mlserver.settings import ModelSettings, Settings
from mlserver.types import InferenceRequest

from ..utils import RESTClient


async def test_live(rest_client: RESTClient):
    is_live = await rest_client.live()
    is_ready = await rest_client.ready()

    # Assert that the server is live, but some models are still loading
    assert is_live
    assert not is_ready


async def test_infer(
    rest_client: RESTClient,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    await rest_client.wait_until_model_ready(sum_model_settings.name)
    await rest_client.infer(sum_model_settings.name, inference_request)
