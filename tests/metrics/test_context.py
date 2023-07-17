import pytest
import asyncio
import random

from typing import Optional
from prometheus_client import Histogram

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.metrics.registry import MetricsRegistry
from mlserver.metrics.errors import InvalidModelContext
from mlserver.metrics.context import (
    SELDON_MODEL_NAME_LABEL,
    SELDON_MODEL_VERSION_LABEL,
    register,
    log,
    _get_labels_from_context,
)
from mlserver.context import model_context

from ..fixtures import SumModel


@pytest.fixture
def sum_model_context(sum_model_settings: ModelSettings) -> ModelSettings:
    with model_context(sum_model_settings):
        yield sum_model_settings


@pytest.mark.parametrize(
    "name, version, expected",
    [
        (
            "foo",
            "v1.0",
            {SELDON_MODEL_NAME_LABEL: "foo", SELDON_MODEL_VERSION_LABEL: "v1.0"},
        ),
        ("foo", None, {SELDON_MODEL_NAME_LABEL: "foo", SELDON_MODEL_VERSION_LABEL: ""}),
    ],
)
def test_model_context(name: str, version: Optional[str], expected: dict):
    model_settings = ModelSettings(
        name=name, implementation=SumModel, parameters=ModelParameters(version=version)
    )
    with pytest.raises(InvalidModelContext):
        _get_labels_from_context()

    with model_context(model_settings):
        labels = _get_labels_from_context()
        assert labels == expected

    with pytest.raises(InvalidModelContext):
        _get_labels_from_context()


async def test_model_context_multiple():
    async def _get_labels(model_settings: ModelSettings) -> dict:
        with model_context(model_settings):
            # Force contexts to be overlapped by introducing a random wait
            secs_to_wait = random.random()
            await asyncio.sleep(secs_to_wait)
            return _get_labels_from_context()

    models_settings = [
        ModelSettings(name=f"model-{idx}", implementation=SumModel) for idx in range(10)
    ]

    models_labels = await asyncio.gather(
        *[_get_labels(model_settings) for model_settings in models_settings]
    )

    assert len(models_labels) == len(models_settings)
    for model_settings, model_labels in zip(models_settings, models_labels):
        assert model_labels[SELDON_MODEL_NAME_LABEL] == model_settings.name
        assert model_labels[SELDON_MODEL_VERSION_LABEL] == ""


def test_register(metrics_registry: MetricsRegistry, sum_model_context: ModelSettings):
    register("foo", "My custom description")

    assert "foo" in metrics_registry

    metric = metrics_registry["foo"]
    assert isinstance(metric, Histogram)
    assert metric._documentation == "My custom description"


def test_log(metrics_registry: MetricsRegistry, sum_model_context: ModelSettings):
    log(foo=3.2)

    assert "foo" in metrics_registry

    metric = metrics_registry["foo"]
    assert isinstance(metric, Histogram)
    assert len(metric._metrics) == 1
    labeled_metric = metric._metrics[
        (sum_model_context.name, sum_model_context.version)
    ]
    assert labeled_metric._sum._value == 3.2
