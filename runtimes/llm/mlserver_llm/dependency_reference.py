from dataclasses import dataclass
from typing import Dict, Union

from common import LLMProviderList


@dataclass
class LLMDependencyReference:
    """Class for keeping track of dependencies required to OpenAI."""

    provider_id: str
    runtime_class: str


_TAG_TO_RT_IMPL: Dict[str, LLMDependencyReference] = {
    "openai": LLMDependencyReference(
        provider_id="openai",
        runtime_class="mlserver_llm.openai.openai_runtime.OpenAIRuntime",
    ),
}


def get_openai_class_as_str(tag: str) -> str:
    return _TAG_TO_RT_IMPL[tag].openai_class


def get_mlmodel_class_as_str(tag: Union[LLMProviderList, str]) -> str:
    if isinstance(tag, LLMProviderList):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag].runtime_class
