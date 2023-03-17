from dataclasses import dataclass
from importlib import import_module
from typing import Dict, Union

from .common import LLMProviderEnum


@dataclass
class LLMDependencyReference:
    """Class for keeping track of dependencies required to LLM providers."""

    provider_id: str
    runtime_class: str


_TAG_TO_RT_IMPL: Dict[str, LLMDependencyReference] = {
    "openai": LLMDependencyReference(
        provider_id="openai",
        runtime_class="mlserver_llm.openai.openai_runtime.OpenAIRuntime",
    ),
}


def get_mlmodel_class_as_str(tag: Union[LLMProviderEnum, str]) -> str:
    if isinstance(tag, LLMProviderEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag].runtime_class


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1 :])
    return klass
