from dataclasses import dataclass
from enum import Enum
from typing import Union, Dict


@dataclass
class ExplainerDependencyReference:
    """Class for keeping track of dependencies required to Alibi runtime."""

    explainer_name: str
    alibi_class: str
    runtime_class: str


_ANCHOR_IMAGE_TAG = "anchor_image"
_ANCHOR_TEXT_TAG = "anchor_text"
_ANCHOR_TABULAR_TAG = "anchor_tabular"
_INTEGRATED_GRADIENTS_TAG = "integrated_gradients"


# NOTE: to add new explainers populate the below dict with a new
# ExplainerDependencyReference, referencing the specific runtime class in mlserver
# and the specific alibi explain class.
# this can be simplified when alibi moves to a config based init.

_BLACKBOX_MODULDE = "mlserver_alibi_explain.explainers.black_box_runtime"
_INTEGRATED_GRADIENTS_MODULE = "mlserver_alibi_explain.explainers.integrated_gradients"

_TAG_TO_RT_IMPL: Dict[str, ExplainerDependencyReference] = {
    _ANCHOR_IMAGE_TAG: ExplainerDependencyReference(
        explainer_name=_ANCHOR_IMAGE_TAG,
        runtime_class=f"{_BLACKBOX_MODULDE}.AlibiExplainBlackBoxRuntime",
        alibi_class="alibi.explainers.AnchorImage",
    ),
    _ANCHOR_TABULAR_TAG: ExplainerDependencyReference(
        explainer_name=_ANCHOR_TABULAR_TAG,
        runtime_class=f"{_BLACKBOX_MODULDE}.AlibiExplainBlackBoxRuntime",
        alibi_class="alibi.explainers.AnchorTabular",
    ),
    _ANCHOR_TEXT_TAG: ExplainerDependencyReference(
        explainer_name=_ANCHOR_TEXT_TAG,
        runtime_class=f"{_BLACKBOX_MODULDE}.AlibiExplainBlackBoxRuntime",
        alibi_class="alibi.explainers.AnchorText",
    ),
    _INTEGRATED_GRADIENTS_TAG: ExplainerDependencyReference(
        explainer_name=_INTEGRATED_GRADIENTS_TAG,
        runtime_class=f"{_INTEGRATED_GRADIENTS_MODULE}.IntegratedGradientsWrapper",
        alibi_class="alibi.explainers.IntegratedGradients",
    ),
}


class ExplainerEnum(str, Enum):
    anchor_image = _ANCHOR_IMAGE_TAG
    anchor_text = _ANCHOR_TEXT_TAG
    anchor_tabular = _ANCHOR_TABULAR_TAG
    integrated_gradients = _INTEGRATED_GRADIENTS_TAG


def get_mlmodel_class_as_str(tag: Union[ExplainerEnum, str]) -> str:
    if isinstance(tag, ExplainerEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag].runtime_class


def get_alibi_class_as_str(tag: Union[ExplainerEnum, str]) -> str:
    if isinstance(tag, ExplainerEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag].alibi_class
