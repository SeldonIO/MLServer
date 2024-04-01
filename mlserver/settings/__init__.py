from mlserver.pydantic_migration import is_pydantic_v1
from typing import TYPE_CHECKING

from mlserver.settings.commons import CORSSettings, Settings, ModelParameters


if TYPE_CHECKING:
    from mlserver.settings.settings_v2 import ModelSettings
else:
    if is_pydantic_v1():
        from mlserver.settings.settings_v1 import ModelSettings
    else:
        from mlserver.settings.settings_v2 import ModelSettings


__all__ = (
    "CORSSettings",
    "Settings",
    "ModelParameters",
    "ModelSettings",
)
