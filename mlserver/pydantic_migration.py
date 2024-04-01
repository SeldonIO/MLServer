# noqa: F401
from typing import TYPE_CHECKING
from pydantic import VERSION


def is_pydantic_v1():
    return VERSION.startswith("1.")


if TYPE_CHECKING:
    from pydantic.types import ImportString as PyObject
    from pydantic_settings import BaseSettings
else:
    if is_pydantic_v1():
        from pydantic import PyObject
        from pydantic import BaseSettings
    else:
        from pydantic.types import ImportString as PyObject
        from pydantic_settings import BaseSettings
