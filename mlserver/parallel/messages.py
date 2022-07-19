from enum import IntEnum
from pydantic import BaseModel
from typing import Optional

from ..types import InferenceRequest, InferenceResponse, MetadataModelResponse
from ..settings import ModelSettings


class ModelUpdateType(IntEnum):
    Load = 1
    Unload = 2


class ModelRequestMessage(BaseModel):
    id: str
    model_name: str
    model_version: Optional[str] = None
    inference_request: Optional[InferenceRequest]


class ModelResponseMessage(BaseModel):
    class Config:
        # This is to allow having an Exception field
        arbitrary_types_allowed = True

    id: str
    inference_response: Optional[InferenceResponse]
    metadata_response: Optional[MetadataModelResponse]
    exception: Optional[Exception]


class ModelUpdateMessage(BaseModel):
    update_type: ModelUpdateType
    model_settings: ModelSettings
