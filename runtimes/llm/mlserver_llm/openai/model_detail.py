from dataclasses import dataclass
from typing import Dict

from .common import OpenAIModelTypeEnum


@dataclass
class OpenAIModelDetail:
    """Class for keeping track of dependencies required to OpenAI."""

    model_id: str
    model_type: OpenAIModelTypeEnum


_BASE_MODULE = "openai"

_TAG_TO_RT_IMPL: Dict[str, OpenAIModelDetail] = {
    "gpt-3.5-turbo": OpenAIModelDetail(
        model_id="gpt-3.5-turbo", model_type=OpenAIModelTypeEnum.chat
    ),
}


def get_openai_model_detail(tag: str) -> OpenAIModelDetail:
    return _TAG_TO_RT_IMPL[tag]
