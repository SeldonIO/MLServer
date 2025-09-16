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
from typing import Any, Union, get_args, get_origin, get_type_hints
from pydantic.fields import PydanticUndefined

# Optional overrides for any fields that don't have comments
FIELD_OVERRIDES: Dict[str, Dict[str, str]] = {
    "Settings": {},
    "ModelSettings": {},
    "ModelParameters": {},
}

# ---------------------------
# Small helpers
# ---------------------------
def _type_to_str(tp: Any) -> str:
    """Pretty-print typing annotations: Optional, Union, List, Dict, Literal, etc."""
    if tp is None:
        return "None"
    if isinstance(tp, str):
        return tp
    origin = get_origin(tp)
    args = get_args(tp)
    # Builtins
    if origin is None:
        # Clean module-qualnames like <class 'int'> or typing.Any
        if getattr(tp, "__module__", "") in ("builtins", "typing"):
            return getattr(tp, "__name__", str(tp)).replace("NoneType", "None")
        return getattr(tp, "__name__", str(tp)).replace("NoneType", "None")
    # typing constructs
    name = getattr(origin, "_name", None) or getattr(origin, "__name__", str(origin))
    if origin is Union:
        # Optional[T] is Union[T, None]
        non_none = [a for a in args if a is not type(None)]  # noqa: E721
        if len(args) == 2 and len(non_none) == 1:
            return f"Optional[{_type_to_str(non_none[0])}]"
        return "Union[" + ", ".join(_type_to_str(a) for a in args) + "]"
    if name in ("List", "list"):
        return f"List[{_type_to_str(args[0])}]" if args else "List[Any]"
    if name in ("Dict", "dict"):
        return f"Dict[{_type_to_str(args[0])}, {_type_to_str(args[1])}]" if len(args) == 2 else "Dict[Any, Any]"
    if name in ("Tuple", "tuple"):
        return "Tuple[" + ", ".join(_type_to_str(a) for a in args) + "]" if args else "Tuple"
    if name == "Literal":
        return "Literal[" + ", ".join(repr(a) for a in args) + "]"
    return f"{name}[" + ", ".join(_type_to_str(a) for a in args) + "]" if args else name

def _format_default(field: Any) -> str:
    """Default rendering for Pydantic v2 fields."""
    if getattr(field, "default", PydanticUndefined) is not PydanticUndefined:
        return repr(field.default)
    factory = getattr(field, "default_factory", None)
    if factory is not None:
        return "<factory>"
    return "-"

def _format_signature(func) -> str:
    """Build a nicer signature: resolve ForwardRef and typing to readable strings."""
    try:
        hints = get_type_hints(func)
    except Exception:
        hints = {}
    sig = inspect.signature(func)
    parts = []
    for name, param in sig.parameters.items():
        ann = hints.get(name, param.annotation)
        ann_str = "" if ann is inspect._empty else f": {_type_to_str(ann)}"
        if param.default is not inspect._empty:
            parts.append(f"{name}{ann_str} = {repr(param.default)}")
        else:
            parts.append(f"{name}{ann_str}")
    ret_ann = hints.get("return", sig.return_annotation)
    ret_str = "" if ret_ann is inspect._empty else f" -> {_type_to_str(ret_ann)}"
    return f"{func.__name__}(" + ", ".join(parts) + ")" + ret_str

# ---------------------------
# Pydantic model docs
# ---------------------------
def document_pydantic_model(model_cls: Type[Any], source_path: str = None) -> str:
    """
    Generate Markdown for a Pydantic v2 model:
    - Config section (with attribute type + default)
    - Fields section (alphabetical), with type, default, description
    """
    lines: list[str] = []

    # --- Config ---
    lines.append("### Config\n")
    lines.append("| Attribute | Type | Default |")
    lines.append("|-----------|------|---------|")
    config = getattr(model_cls, "model_config", {}) or {}
    # Access as dict to get real values
    config_attrs = {
        "extra": ("str", "ignore"),
        "env_prefix": ("str", "MLSERVER_"),
        "env_file": ("str", ".env"),
        "protected_namespaces": ("tuple", "()"),
    }
    for attr, (attr_type, default) in config_attrs.items():
        value = config.get(attr, default) if isinstance(config, dict) else getattr(config, attr, default)
        value_repr = f'"{value}"' if isinstance(value, str) else repr(value) if value is not None else "-"
        lines.append(f"| `{attr}` | `{attr_type}` | `{value_repr}` |")

    lines.append("")  # spacing

    # --- Model docstring (if any) ---
    if model_cls.__doc__:
        lines.append(f"**Model Description:** {inspect.cleandoc(model_cls.__doc__)}\n")

    # --- Fields ---
    lines.append("### Fields\n")
    lines.append("| Field | Type | Default | Description |")
    lines.append("|-------|------|---------|-------------|")

    model_name = model_cls.__name__
    overrides = FIELD_OVERRIDES.get(model_name, {})

    sorted_fields = sorted(model_cls.model_fields.items(), key=lambda item: item[0])
    for name, field in sorted_fields:
        ftype = _type_to_str(getattr(field, "annotation", Any))
        default = _format_default(field)
        desc = getattr(field, "description", None) or overrides.get(name, "-")
        lines.append(f"| `{name}` | `{ftype}` | `{default}` | {desc} |")

    return "\n".join(lines)

# ---------------------------
# Classes and modules
# ---------------------------
def document_class_or_module(obj: Union[type, ModuleType],
                             include_private: bool = False,
                             include_inherited: bool = False,
                             add_top_title: bool = False) -> str:
    """
    Render methods for classes, and classes + functions for modules.
    - Method headings use 'name()' for GitBook RHS nav.
    - Full signature is shown in a Python block.
    - Omits empty sections.
    - Does not add a top-level H1 unless add_top_title=True.
    """
    lines: list[str] = []

    if inspect.isclass(obj):
        if add_top_title:
            lines.append(f"# {obj.__name__}\n")
            if obj.__doc__:
                lines.append(inspect.cleandoc(obj.__doc__) + "\n")

        # Collect methods
        method_blocks: list[str] = []
        for name, func in inspect.getmembers(obj, inspect.isfunction):
            if not include_private and name.startswith("_"):
                continue
            if not include_inherited and func.__qualname__.split(".")[0] != obj.__name__:
                continue
            doc = inspect.getdoc(func) or "_No description available._"
            sig_str = _format_signature(func)
            method_blocks.append(f"### {name}()\n")
            method_blocks.append(f"```python\n{sig_str}\n```\n")
            method_blocks.append(f"{doc}\n")

        if method_blocks:
            lines.append("## Methods\n")
            lines.extend(method_blocks)
        return "\n".join(lines)

    if inspect.ismodule(obj):
        if add_top_title:
            lines.append(f"# {obj.__name__}\n")
            if obj.__doc__:
                lines.append(inspect.cleandoc(obj.__doc__) + "\n")

        # Classes
        class_sections: list[str] = []
        for cname, cls in inspect.getmembers(obj, inspect.isclass):
            if not include_private and cname.startswith("_"):
                continue
            section: list[str] = [f"## {cname}\n"]
            if cls.__doc__:
                section.append(inspect.cleandoc(cls.__doc__) + "\n")
            # Methods inside the class
            method_blocks: list[str] = []
            for mname, func in inspect.getmembers(cls, inspect.isfunction):
                if not include_private and mname.startswith("_"):
                    continue
                doc = inspect.getdoc(func) or "_No description available._"
                sig_str = _format_signature(func)
                method_blocks.append(f"### {mname}()\n")
                method_blocks.append(f"```python\n{sig_str}\n```\n")
                method_blocks.append(f"{doc}\n")
            if method_blocks:
                section.append("### Methods\n")
                section.extend(method_blocks)
            class_sections.append("\n".join(section))

        if class_sections:
            lines.extend(class_sections)

        # Standalone functions
        func_sections: list[str] = []
        for fname, func in inspect.getmembers(obj, inspect.isfunction):
            if not include_private and fname.startswith("_"):
                continue
            doc = inspect.getdoc(func) or "_No description available._"
            sig_str = _format_signature(func)
            func_sections.append(f"## {fname}()\n")
            func_sections.append(f"```python\n{sig_str}\n```\n")
            func_sections.append(f"{doc}\n")

        if func_sections:
            lines.extend(func_sections)

        return "\n".join(lines)

    raise TypeError(f"Object {obj} is not a class or module")

# ---------------------------
# Main driver
# ---------------------------
def main():
    outdir = "./docs-gb/api"
    os.makedirs(outdir, exist_ok=True)

    targets = [
        (Settings, "Settings", True, "mlserver/settings.py"),
        (ModelSettings, "ModelSettings", True, "mlserver/settings.py"),
        (ModelParameters, "ModelParameters", True, "mlserver/settings.py"),
        (MLModel, "MLModel", False, "mlserver/model.py"),
        (Types, "Types", False, "mlserver/types.py"),
        (Codecs, "Codecs", False, "mlserver/codecs.py"),
        (Metrics, "Metrics", False, "mlserver/metrics.py"),
    ]

    for obj, name, is_pydantic, source_path in targets:
        print(f"Generating docs for {name}...")
        filepath = os.path.join(outdir, f"{name}.md")
        with open(filepath, "w") as f:
            # Single H1 per page
            f.write(f"# {name}\n\n")

            # Top-level docstring (class or module)
            if getattr(obj, "__doc__", None):
                f.write(inspect.cleandoc(obj.__doc__) + "\n\n")

            if is_pydantic:
                # Titles are included by document_pydantic_model (### Config, ### Fields)
                f.write(document_pydantic_model(obj, source_path) + "\n")
            else:
                # Classes: show Methods section if available
                if inspect.isclass(obj):
                    methods_md = document_class_or_module(obj, add_top_title=False)
                    if methods_md.strip():
                        f.write("## Methods\n\n")  # section title once
                        # document_class_or_module already adds ### method() blocks
                        # but not the "## Methods" header when add_top_title=False
                        # so remove our just-added header and write content directly
                        # We already wrote the header; ensure we don't duplicate
                        # Instead, re-call and write without adding "## Methods"
                        f.seek(f.tell() - len("## Methods\n\n"))
                        f.write(document_class_or_module(obj, add_top_title=False))
                else:
                    # Modules: let helper render classes + functions (no duplicate H1)
                    module_md = document_class_or_module(obj, add_top_title=False)
                    if module_md.strip():
                        f.write(module_md + "\n")

    print("Docs generated in docs-gb/api/")

if __name__ == "__main__":
    main()
