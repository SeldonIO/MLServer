from enum import IntEnum
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from ..settings import ModelSettings


class ModelUpdateType(IntEnum):
    Load = 1
    Unload = 2


class ModelRequestMessage(BaseModel):
    id: str
    model_name: str
    model_version: Optional[str] = None
    method_name: str
    method_args: List[Any] = []
    method_kwargs: Dict[str, Any] = {}


class ModelResponseMessage(BaseModel):
    class Config:
        # This is to allow having an Exception field
        arbitrary_types_allowed = True

    id: str
    return_value: Optional[Any]
    exception: Optional[Exception]


class ModelUpdateMessage(BaseModel):
    update_type: ModelUpdateType
    model_settings: ModelSettings
