import os

import pytest

from mlserver.settings import ModelSettings, ModelParameters
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntime

TESTS_PATH = os.path.dirname(__file__)


# TODO: how to make this in utils?
def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
async def anchor_image_runtime() -> AlibiExplainRuntime:
    rt = AlibiExplainRuntime(
        ModelSettings(
            parallel_workers=1,
            parameters=ModelParameters(
                uri="./data/mnist_anchor_image",
                extra=AlibiExplainSettings(
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
async def integrated_gradients_runtime() -> AlibiExplainRuntime:
    rt = AlibiExplainRuntime(
        ModelSettings(
            parallel_workers=1,
            parameters=ModelParameters(
                # uri="./data/mnist_anchor_image",
                extra=AlibiExplainSettings(
                    init_parameters={
                        "n_steps": 50,
                        "method": "gausslegendre"
                    },
                    explainer_type="integrated_gradients",
                    infer_uri="./data/tf_mnist_ig/model.h5"
                )
            )
        )
    )
    await rt.load()

    return rt

