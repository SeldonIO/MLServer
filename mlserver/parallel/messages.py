import json

from asyncio import CancelledError
from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union

from ..utils import get_import_path, generate_uuid
from ..settings import ModelSettings


class ModelUpdateType(IntEnum):
    Load = 1
    Unload = 2


class Message(BaseModel):
    id: str = Field(default_factory=generate_uuid)


class ModelRequestMessage(Message):

    model_name: str
    model_version: Optional[str] = None
    method_name: str
    method_args: List[Any] = []
    method_kwargs: Dict[str, Any] = {}


class ModelResponseMessage(Message):
    class Config:
        # This is to allow having an Exception field
        arbitrary_types_allowed = True

    return_value: Optional[Any]
    exception: Optional[Union[Exception, CancelledError]]


class ModelUpdateMessage(Message):

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
