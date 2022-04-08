from enum import IntEnum
from pydantic import BaseModel
from typing import Optional

from ..types import InferenceRequest, InferenceResponse
from ..settings import ModelSettings


class ModelUpdateType(IntEnum):
    Load = 1
    Unload = 2


class InferenceRequestMessage(BaseModel):
    id: str
    model_name: str
    model_version: Optional[str] = None
    inference_request: InferenceRequest


class InferenceResponseMessage(BaseModel):
    id: str
    inference_response: InferenceResponse


class ModelUpdateMessage(BaseModel):
    update_type: ModelUpdateType
    model_settings: ModelSettings
