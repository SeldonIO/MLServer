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
        protected_namespaces=(),
        use_enum_values=True,
    )

    def model_dump(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().model_dump(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )

    def model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().model_dump_json(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )
