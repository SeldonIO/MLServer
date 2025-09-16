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
def document_class_or_module(obj: Union[type, ModuleType],
                             include_private: bool = False,
                             include_inherited: bool = False) -> str:
    """
    Generate GitBook-friendly Markdown documentation for a class or module.

    Classes:
        - Methods: name, signature (code block), docstring

    Modules:
        - Functions and classes

    Args:
        include_private: include _private methods/functions
        include_inherited: include inherited methods for classes
    """
    lines = []

    if inspect.isclass(obj):
        lines.append(f"# Class `{obj.__name__}`\n")
        if obj.__doc__:
            lines.append(inspect.cleandoc(obj.__doc__) + "\n")
        
        lines.append("## Methods\n")
        for name, func in inspect.getmembers(obj, inspect.isfunction):
            if not include_private and name.startswith("_"):
                continue
            if not include_inherited and func.__qualname__.split(".")[0] != obj.__name__:
                continue
            
            sig = inspect.signature(func)
            doc = inspect.getdoc(func) or "-"
            
            # Add method heading
            lines.append(f"### `{name}`\n")
            
            # Add signature in a code block, wrapped nicely
            sig_str = str(sig)
            # Optional: wrap long signatures manually (e.g., 80 chars)
            # For now just show as code block
            lines.append("```python")
            lines.append(f"{name}{sig_str}")
            lines.append("```\n")
            
            # Add docstring
            lines.append(doc + "\n")
    
    elif inspect.ismodule(obj):
        lines.append(f"# Module `{obj.__name__}`\n")
        if obj.__doc__:
            lines.append(inspect.cleandoc(obj.__doc__) + "\n")
        
        # Document classes
        for name, cls in inspect.getmembers(obj, inspect.isclass):
            if not include_private and name.startswith("_"):
                continue
            lines.append(f"## Class `{name}`\n")
            if cls.__doc__:
                lines.append(inspect.cleandoc(cls.__doc__) + "\n")
            lines.append("### Methods\n")
            for mname, func in inspect.getmembers(cls, inspect.isfunction):
                if not include_private and mname.startswith("_"):
                    continue
                sig = inspect.signature(func)
                doc = inspect.getdoc(func) or "-"
                lines.append(f"#### `{mname}`\n")
                lines.append("```python")
                lines.append(f"{mname}{sig}")
                lines.append("```\n")
                lines.append(doc + "\n")
        
        # Document standalone functions
        for name, func in inspect.getmembers(obj, inspect.isfunction):
            if not include_private and name.startswith("_"):
                continue
            sig = inspect.signature(func)
            doc = inspect.getdoc(func) or "-"
            lines.append(f"## Function `{name}`\n")
            lines.append("```python")
            lines.append(f"{name}{sig}")
            lines.append("```\n")
            lines.append(doc + "\n")
    
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
