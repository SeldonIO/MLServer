import os
import inspect
import pdoc

from mlserver.settings import Settings, ModelSettings, ModelParameters  # Import ModelParameters
from mlserver.model import MLModel
import mlserver.types as Types
import mlserver.codecs as Codecs
import mlserver.metrics as Metrics

from typing import Any, Dict
import ast
from pathlib import Path
from typing import Dict, Type, Any

import inspect
from types import ModuleType
from typing import Any, Union


# Optional overrides for any fields that don't have comments
FIELD_OVERRIDES: Dict[str, Dict[str, str]] = {
    "Settings": {
        # Add overrides here if needed
    },
    "ModelSettings": {
        # Add overrides here if needed
    },
}

def document_pydantic_model(model_cls: Type[Any], source_path: str = None) -> str:
    """
    Generate a Markdown table for a Pydantic v2 model, including:
    - Config settings (extra, env_prefix, env_file, etc.)
    - Field types, defaults, and descriptions from Field(description=...) or FIELD_OVERRIDES.
    Fields are sorted alphabetically by name.
    """
    lines = []

    lines.append("### Config\n")
    lines.append("| Attribute | Type | Default |")
    lines.append("|-----------|------|---------|")

    # Pydantic v2: model_config is a ConfigDict
    config = getattr(model_cls, "model_config", {})

    config_attrs = {
        "extra": ("str", "ignore"),
        "env_prefix": ("str", "MLSERVER_"),
        "env_file": ("str", ".env"),
        "protected_namespaces": ("tuple", "()"),
    }

    for attr, (attr_type, default) in config_attrs.items():
        # Use the actual value from config if available, fallback to default
        value = getattr(config, attr, default)
        # For strings, wrap in quotes to match Python syntax
        if isinstance(value, str):
            value_repr = f'"{value}"'
        else:
            value_repr = str(value)
        lines.append(f"| `{attr}` | `{attr_type}` | `{value_repr}` |")

    lines.append("")  # empty line for spacing

    # --- Add model docstring ---
    if model_cls.__doc__:
        docstring = model_cls.__doc__.strip()
        lines.append(f"**Model Description:** {docstring}\n")

    # --- Add Fields table ---
    lines.append("### Fields\n")
    lines.append("| Field | Type | Default | Description |")
    lines.append("|-------|------|---------|-------------|")

    model_name = model_cls.__name__
    overrides = FIELD_OVERRIDES.get(model_name, {})

    sorted_fields = sorted(model_cls.model_fields.items(), key=lambda item: item[0])

    for name, field in sorted_fields:
        # Type
        field_type = getattr(field.annotation, "__name__", str(field.annotation))
        # Default
        default = field.default if field.default is not None else "-"
        if callable(default):
            default = "<callable>"
        # Description: Field.description first, then override
        desc = field.description or overrides.get(name, "-")
        # Add row
        lines.append(f"| `{name}` | `{field_type}` | `{default}` | {desc} |")

    return "\n".join(lines)

    
# ---------------------------
# Helpers for normal classes
# ---------------------------
import inspect
from types import ModuleType
from typing import Any, Union


def document_class_or_module(obj: Union[type, ModuleType],
                             include_private: bool = False,
                             include_inherited: bool = False) -> str:
    """
    Generate GitBook-friendly Markdown documentation for a class or module.
    Handles classes, modules, static/class/instance methods.
    Avoids empty sections and duplicated headings.
    """
    lines = []

    def format_signature(func):
        return str(inspect.signature(func))

    def document_method(name, func):
        sig_str = format_signature(func)
        doc = inspect.getdoc(func) or "-"
        return "\n".join([
            f"### `{name}`",
            "```python",
            f"{name}{sig_str}",
            "```",
            doc + "\n"
        ])

    if inspect.isclass(obj):
        # Document class
        lines.append(f"# Class `{obj.__name__}`\n")
        if obj.__doc__:
            lines.append(inspect.cleandoc(obj.__doc__) + "\n")

        # Gather all methods first
        methods = []
        for name, member in inspect.getmembers(obj):
            if not include_private and name.startswith("_"):
                continue
            if not include_inherited and inspect.isfunction(member):
                if member.__qualname__.split(".")[0] != obj.__name__:
                    continue
            if inspect.isfunction(member) or inspect.ismethod(member):
                methods.append(document_method(name, member))
            elif isinstance(member, (staticmethod, classmethod)):
                methods.append(document_method(name, member.__func__))

        # Only add Methods section if there are any
        if methods:
            lines.append("## Methods\n")
            lines.extend(methods)

    elif inspect.ismodule(obj):
        lines.append(f"# Module `{obj.__name__}`\n")
        if obj.__doc__:
            lines.append(inspect.cleandoc(obj.__doc__) + "\n")

        # Document classes first
        for name, cls in inspect.getmembers(obj, inspect.isclass):
            if not include_private and name.startswith("_"):
                continue

            # Only document classes defined in this module
            if cls.__module__ != obj.__name__:
                continue

            lines.append(f"## Class `{name}`\n")
            if cls.__doc__:
                lines.append(inspect.cleandoc(cls.__doc__) + "\n")

            # Gather methods
            methods = []
            for mname, member in inspect.getmembers(cls):
                if not include_private and mname.startswith("_"):
                    continue
                if inspect.isfunction(member) or inspect.ismethod(member):
                    methods.append(document_method(mname, member))
                elif isinstance(member, (staticmethod, classmethod)):
                    methods.append(document_method(mname, member.__func__))
            if methods:
                lines.append("### Methods\n")
                lines.extend(methods)

        # Document top-level functions
        functions = []
        for name, member in inspect.getmembers(obj, inspect.isfunction):
            if not include_private and name.startswith("_"):
                continue
            functions.append(document_method(name, member))

        if functions:
            lines.append("## Functions\n")
            lines.extend(functions)

    else:
        raise TypeError(f"Object {obj} is not a class or module")

    return "\n".join(lines)


# ---------------------------
# Main driver
# ---------------------------
def main():
    outdir = "./docs-gb/api"
    os.makedirs(outdir, exist_ok=True)

    # Classes to document
    targets = [
        (Settings, "Settings", True, "mlserver/settings.py"),
        (ModelSettings, "ModelSettings", True, "mlserver/settings.py"),
        (ModelParameters, "ModelParameters", True, "mlserver/settings.py"),  # Added ModelParameters
        (MLModel, "MLModel", False, "mlserver/model.py"),
        (Types, "Types", False, "mlserver/types.py"),
        (Codecs, "Codecs", False, "mlserver/codecs.py"),
        (Metrics, "Metrics", False, "mlserver/metrics.py"),
    ]

    for cls, name, is_pydantic, source_path in targets:
        print(f"Generating docs for {name}...")
        filepath = os.path.join(outdir, f"{name}.md")
        with open(filepath, "w") as f:
            f.write(f"# {name}\n\n")

            # Add docstring
            if cls.__doc__:
                f.write(inspect.cleandoc(cls.__doc__) + "\n\n")

            # Special case: pydantic settings
            if is_pydantic:
                f.write("## Fields\n\n")
                # Pass the source_path to document_pydantic_model
                f.write(document_pydantic_model(cls, source_path) + "\n\n")
            else:
                f.write("## Methods\n\n")
                # Use document_class_or_module instead of document_class
                f.write(document_class_or_module(cls) + "\n\n")

    print("Docs generated in docs-gb/api/")


if __name__ == "__main__":
    main()
