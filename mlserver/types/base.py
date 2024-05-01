import pydantic
from pydantic import ConfigDict


class BaseModel(pydantic.BaseModel):
    """
    Override Pydantic's BaseModel class to ensure all payloads exclude unset
    fields by default.

    From:
        https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525
    """

    model_config = ConfigDict(
        use_enum_values=True,
    )

    def dict(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().dict(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )

    def json(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().json(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )
