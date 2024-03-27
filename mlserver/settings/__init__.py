from mlserver.pydantic_migration import is_pydantic_v1

if is_pydantic_v1():
    from mlserver.settings.settings_v1 import *
else:
    from mlserver.settings.settings_v2 import *
