import os

import pytest

from mlserver_alibi_explain.explainers.anchor_image import AnchorImageWrapper
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver.settings import ModelSettings, ModelParameters

TESTS_PATH = os.path.dirname(__file__)


# TODO: how to make this in utils?
def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
async def runtime() -> AnchorImageWrapper:
    rt = AnchorImageWrapper(
        ModelSettings(
            parameters=ModelParameters(
                extra=AlibiExplainSettings(
                    init_explainer=True,
                    init_parameters={
                        "segmentation_fn": "slic",
                        "segmentation_kwargs": {"n_segments": 15, "compactness": 20, "sigma": .5},
                        "image_shape": (28, 28, 1),
                        "images_background": None
                    },
                    explainer_type="anchor_image",
                    infer_uri="http://localhost:36307/v2/models/test-pytorch-mnist/infer"
                )
            )
        )
    )
    await rt.load()

    return rt

