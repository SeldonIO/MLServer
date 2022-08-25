import json

from enum import IntEnum
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from ..utils import get_import_path
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
    serialised_model_settings: str

    def __init__(self, *args, **kwargs):
        model_settings = kwargs.pop("model_settings", None)
        if model_settings:
            as_dict = model_settings.dict()
            # Ensure the private `_source` attr also gets serialised
            if model_settings._source:
                as_dict["_source"] = model_settings._source

            import_path = get_import_path(model_settings.implementation)
            as_dict["implementation"] = import_path
            kwargs["serialised_model_settings"] = json.dumps(as_dict)
        return super().__init__(*args, **kwargs)

    @property
    def model_settings(self) -> ModelSettings:
        return ModelSettings.parse_raw(self.serialised_model_settings)
