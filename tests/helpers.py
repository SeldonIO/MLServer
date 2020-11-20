from typing import Type


def get_import_path(klass: Type):
    return f"{klass.__module__}.{klass.__name__}"
