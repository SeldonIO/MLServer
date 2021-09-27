import os

import pytest

from mlserver_alibi_explain.explainers.anchor_image import AnchorImageWrapper
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver.settings import ModelSettings, ModelParameters
from mlserver_alibi_explain.explainers.integrated_gradients import IntegratedGradientsWrapper

TESTS_PATH = os.path.dirname(__file__)


# TODO: how to make this in utils?
def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
async def anchor_image_runtime() -> AnchorImageWrapper:
    rt = AnchorImageWrapper(
        ModelSettings(
            parameters=ModelParameters(
                # uri="./data/mnist_anchor_image",
                extra=AlibiExplainSettings(
                    init_explainer=True,
                    init_parameters={
                        "segmentation_fn": "slic",
                        "segmentation_kwargs": {"n_segments": 15, "compactness": 20, "sigma": .5},
                        "image_shape": (28, 28, 1),
                        "images_background": None
                    },
                    # TODO: do we really need this if we have a wrapper per explainer?
                    explainer_type="anchor_image",
                    # TODO: find a way to get the url in test
                    infer_uri="http://localhost:42315/v2/models/test-pytorch-mnist/infer"
                )
            )
        )
    )
    await rt.load()

    return rt


@pytest.fixture
async def integrated_gradients_runtime() -> IntegratedGradientsWrapper:
    rt = IntegratedGradientsWrapper(
        ModelSettings(
            parameters=ModelParameters(
                # uri="./data/mnist_anchor_image",
                extra=AlibiExplainSettings(
                    init_explainer=True,
                    init_parameters={
                        "n_steps": 50,
                        "method": "gausslegendre"
                    },
                    # TODO: do we really need this if we have a wrapper per explainer?
                    explainer_type="anchor_image",
                    # TODO: find a way to get the url in test
                )
            )
        )
    )
    await rt.load()

    return rt

