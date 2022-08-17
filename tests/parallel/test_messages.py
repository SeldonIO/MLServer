import pytest
import json

from mlserver.settings import ModelSettings
from mlserver.parallel.messages import (
    ModelUpdateMessage,
    ModelUpdateType,
)

from ..fixtures import SumModel

# Used to fill in all the default values
_dummy_model_settings = ModelSettings(name="foo", implementation=SumModel).dict()


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "update_type": ModelUpdateType.Load,
                "model_settings": ModelSettings(name="foo", implementation=SumModel),
            },
            ModelUpdateMessage(
                update_type=ModelUpdateType.Load,
                serialised_model_settings=json.dumps(
                    _dummy_model_settings
                    | {
                        "name": "foo",
                        "implementation": "tests.fixtures.SumModel",
                    }
                ),
            ),
        ),
        (
            {
                "update_type": ModelUpdateType.Load,
                "serialised_model_settings": (
                    '{"name":"foo","implementation":"tests.fixtures.SumModel"}'
                ),
            },
            ModelUpdateMessage(
                update_type=ModelUpdateType.Load,
                serialised_model_settings=(
                    '{"name":"foo","implementation":"tests.fixtures.SumModel"}'
                ),
            ),
        ),
    ],
)
def test_model_update_message(kwargs: dict, expected: ModelUpdateMessage):
    model_update_message = ModelUpdateMessage(**kwargs)
    assert model_update_message == expected


@pytest.mark.parametrize(
    "model_update_message, expected",
    [
        (
            ModelUpdateMessage(
                update_type=ModelUpdateType.Load,
                model_settings=ModelSettings(name="foo", implementation=SumModel),
            ),
            ModelSettings(name="foo", implementation=SumModel),
        ),
        (
            ModelUpdateMessage(
                update_type=ModelUpdateType.Load,
                serialised_model_settings=(
                    '{"name":"foo","implementation":"tests.fixtures.SumModel"}'
                ),
            ),
            ModelSettings(name="foo", implementation=SumModel),
        ),
    ],
)
def test_model_settings(
    model_update_message: ModelUpdateMessage, expected: ModelSettings
):
    assert model_update_message.model_settings == expected
