# noqa: F401
from pydantic import VERSION, Field


def is_pydantic_v1():
    return VERSION.startswith("1.")


if is_pydantic_v1():
    from pydantic import PyObject
    from pydantic import BaseSettings
else:
    from pydantic.types import ImportString as PyObject
    from pydantic_settings import BaseSettings, SettingsConfigDict
