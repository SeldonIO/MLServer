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
def document_class(cls, include=None, exclude=None):
    """Generate Markdown for class methods, filtering as needed."""
    methods = []
    for name, func in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith("_"):
            continue
        if include and name not in include:
            continue
        if exclude and name in exclude:
            continue
        if func.__qualname__.split(".")[0] != cls.__name__:
            # Skip inherited
            continue
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or ""
        methods.append(f"### `{name}{sig}`\n\n{doc}\n")
    return "\n".join(methods)


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
                f.write(document_class(cls) + "\n\n")

    print("Docs generated in docs-gb/api/")


if __name__ == "__main__":
    main()
