from pydantic import BaseModel as _BaseModel, json as pydantic_json
from enum import Enum


class BaseModel(_BaseModel):
    """
    Override Pydantic's BaseModel class to ensure all payloads exclude unset
    fields by default.

    From:
        https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525
    """

    def dict(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().dict(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )

    def json(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().json(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )


class EnumSettingByName(Enum):
    """
    Allows classes inheriting from EnumByName to be validated by pydantic
    via the enum member name rather than value.

    From:
       https://github.com/pydantic/pydantic/discussions/2980#discussioncomment-1006430
    """

    # Ugliness: we need to monkeypatch pydantic's jsonification of Enums
    pydantic_json.ENCODERS_BY_TYPE[Enum] = lambda e: e.name

    @classmethod
    def __get_validators__(cls):
        # yield our validator
        yield cls._validate

    @classmethod
    def __modify_schema__(cls, schema):
        """Override pydantic using Enum.name for schema enum values"""
        schema["enum"] = list(cls.__members__.keys())

    @classmethod
    def _validate(cls, v):
        """Validate enum reference, `v`.

        We check:
        1. If it is a member of this Enum
        2. If we can find it by name.
        """
        # is the value an enum member?
        try:
            if v in cls:
                return v
        except TypeError:
            pass

        # not a member...look up by name
        try:
            return cls[v]
        except KeyError:
            name = cls.__name__
            expected = list(cls.__members__.keys())
            raise ValueError(
                f"{v} not found for enum {name}. Expected one of: {expected}"
            )
