from dataclasses import dataclass
from typing import Dict

from .common import OpenAIModelTypeEnum


@dataclass
class OpenAIDependencyReference:
    """Class for keeping track of dependencies required to OpenAI."""

    model_id: str
    openai_class: str
    model_type: OpenAIModelTypeEnum


_BASE_MODULE = "openai"

_TAG_TO_RT_IMPL: Dict[str, OpenAIDependencyReference] = {
    "gpt-3.5-turbo": OpenAIDependencyReference(
        model_id="gpt-3.5-turbo",
        openai_class=f"{_BASE_MODULE}.ChatCompletion",
        model_type=OpenAIModelTypeEnum.chat
    ),
}


def get_openai_model_dependency_detail(tag: str) -> OpenAIDependencyReference:
    return _TAG_TO_RT_IMPL[tag]
