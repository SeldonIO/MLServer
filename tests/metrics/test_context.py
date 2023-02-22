import pytest

from typing import Optional
from prometheus_client import Histogram

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.metrics.registry import MetricsRegistry
from mlserver.metrics.context import (
    SELDON_MODEL_NAME_LABEL,
    SELDON_MODEL_VERSION_LABEL,
    register,
    log,
    model_context,
    _get_labels_from_context,
)

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
    with pytest.raises(LookupError):
        _get_labels_from_context()

    with model_context(model_settings):
        labels = _get_labels_from_context()
        assert labels == expected

    with pytest.raises(LookupError):
        _get_labels_from_context()


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
