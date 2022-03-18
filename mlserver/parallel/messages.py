from enum import IntEnum
from pydantic import BaseModel
from typing import Optional

from ..types import InferenceRequest
from ..settings import ModelSettings


class ModelUpdateType(IntEnum):
    Load = 1
    Unload = 2


class InferenceRequestMessage(BaseModel):
    model_name: str
    model_version: Optional[str] = None
    inference_request: InferenceRequest


# NOTE: InferenceResponses don't need a specific message, since the model name
# and version is self-contained within the response payload.


class ModelUpdateMessage(BaseModel):
    update_type: ModelUpdateType
    model_settings: ModelSettings
