from pydantic import BaseModel as _BaseModel

from mlserver.pydantic_migration import is_pydantic_v1


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


if is_pydantic_v1():

    class Config:
        use_enum_values = True

    # MyPy would complain if running under Pydantic 2.x
    BaseModel.Config = Config  # type: ignore

else:
    from pydantic import ConfigDict

    model_config = ConfigDict(use_enum_values=True)
    # MyPy would complain if running under Pydantic 1.x
    BaseModel.model_config = model_config  # type: ignore
