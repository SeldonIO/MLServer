import os
import inspect
import pdoc
import importlib
import pkgutil
import json
import enum
import re
import click

from mlserver.settings import Settings, ModelSettings, ModelParameters  # Import ModelParameters
from mlserver.model import MLModel
import mlserver.types as Types
import mlserver.codecs as Codecs
import mlserver.metrics as Metrics
import mlserver.cli

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
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        # Builtins or C-implemented callables without signatures
        name = getattr(func, "__name__", "<callable>")
        return f"{name}(...)"

    # Drop leading self/cls from display
    params = list(sig.parameters.items())
    if params and params[0][0] in ("self", "cls"):
        params = params[1:]

    parts = []
    for name, param in params:
        ann = hints.get(name, param.annotation)
        ann_str = "" if ann is inspect._empty else f": {_type_to_str(ann)}"
        if param.default is not inspect._empty:
            parts.append(f"{name}{ann_str} = {repr(param.default)}")
        else:
            parts.append(f"{name}{ann_str}")
    ret_ann = hints.get("return", sig.return_annotation)
    ret_str = "" if ret_ann is inspect._empty else f" -> {_type_to_str(ret_ann)}"
    return f"{getattr(func, '__name__', '<callable>')}(" + ", ".join(parts) + ")" + ret_str

def _is_pydantic_model(cls: type) -> bool:
    return hasattr(cls, "model_fields")

def _class_description(cls: type) -> str:
    """
    Prefer the class docstring; otherwise provide a helpful fallback:
    - Enum subclasses: 'An enumeration.'
    - Pydantic models: 'A Pydantic model.'
    """
    doc_attr = getattr(cls, "__doc__", None)
    try:
        is_enum = issubclass(cls, enum.Enum)
    except Exception:
        is_enum = False

    if doc_attr:
        clean = inspect.cleandoc(doc_attr)
        # If this looks like the generic Enum docs, replace with a short label
        if is_enum:
            enum_doc = inspect.getdoc(enum.Enum) or ""
            if clean.strip() == enum_doc.strip() or clean.startswith("Create a collection of name/value pairs."):
                return "An enumeration."
        return clean

    if is_enum:
        return "An enumeration."
    if _is_pydantic_model(cls):
        return "A Pydantic model."
    return ""

def _render_pydantic_fields_for_class(cls: type) -> list[str]:
    lines: list[str] = []
    # Title for fields
    lines.append("| Field | Type | Default | Description |")
    lines.append("|-------|------|---------|-------------|")
    model_name = cls.__name__
    overrides = FIELD_OVERRIDES.get(model_name, {})
    # Sorted alphabetically
    for fname, field in sorted(getattr(cls, "model_fields", {}).items(), key=lambda it: it[0]):
        ftype = _type_to_str(getattr(field, "annotation", Any))
        default = _format_default(field)
        desc = getattr(field, "description", None) or overrides.get(fname, "-")
        lines.append(f"| `{fname}` | `{ftype}` | `{default}` | {desc} |")
    return lines

def _should_include_schema_for_module(module: ModuleType) -> bool:
    # Only include collapsible JSON Schema for the public Types docs
    return getattr(module, "__name__", "") == "mlserver.types"

def _should_include_fields_for_module(module: ModuleType) -> bool:
    # Show Fields tables for all modules, including Types
    return True

def _render_json_schema_block(cls: type) -> list[str]:
    # Pydantic v2: model_json_schema; v1 fallback: schema
    try:
        if hasattr(cls, "model_json_schema"):
            schema = cls.model_json_schema()
        elif hasattr(cls, "schema"):
            schema = cls.schema()
        else:
            schema = None
    except Exception:
        schema = None

    if not schema:
        return []

    pretty = json.dumps(schema, indent=2, ensure_ascii=False)
    return [
        "<details><summary>JSON Schema</summary>\n\n",
        "```json\n",
        f"{pretty}\n",
        "```\n\n",
        "</details>\n",
    ]

def _get_method_doc_from_mro(cls: type, name: str, member: Any) -> str | None:
    """Return the first available docstring for a method, searching the MRO."""
    doc = inspect.getdoc(member)
    if doc:
        return doc
    for base in getattr(cls, "__mro__", ())[1:]:
        try:
            cand = getattr(base, name)
        except Exception:
            continue
        d = inspect.getdoc(cand)
        if d:
            return d
    return None

def _is_codecs_module(module: ModuleType) -> bool:
    return getattr(module, "__name__", "") == "mlserver.codecs"

def _deprecation_info(obj: Any) -> tuple[bool, str | None]:
    """
    Detect if a callable is deprecated.
    - Checks common decorator-set flags.
    - Unwraps decorated objects.
    - Heuristic: 'deprecated' in the docstring.
    - Special-case: detects mlserver.codecs.base.deprecated() wrapper by scanning code constants/closure.
    """
    def check(target: Any) -> tuple[bool, str | None]:
        for flag in ("__deprecated__", "deprecated", "is_deprecated", "_deprecated"):
            if getattr(target, flag, False):
                reason = (
                    getattr(target, "__deprecated_reason__", None)
                    or getattr(target, "deprecated_reason", None)
                    or getattr(target, "_deprecated_reason", None)
                )
                return True, reason
        # Docstring heuristic
        doc = inspect.getdoc(target) or ""
        for line in doc.splitlines():
            if re.search(r"\bdeprecated\b", line, flags=re.IGNORECASE):
                return True, line.strip() or None

        # Detect our custom @deprecated(...) wrapper (uses logger.warning("DEPRECATED! ..."))
        try:
            code = getattr(target, "__code__", None)
            consts = getattr(code, "co_consts", ()) or ()
            if any(isinstance(c, str) and "DEPRECATED" in c.upper() for c in consts):
                # Try to extract the reason from the closure
                reason = None
                closure = getattr(target, "__closure__", None) or ()
                for cell in closure:
                    try:
                        val = cell.cell_contents
                        if isinstance(val, str):
                            reason = val
                            break
                    except Exception:
                        continue
                return True, reason
        except Exception:
            pass

        return False, None

    is_dep, reason = check(obj)
    if is_dep:
        return is_dep, reason
    try:
        unwrapped = inspect.unwrap(obj)
    except Exception:
        unwrapped = None
    if unwrapped is not None and unwrapped is obj:
        return check(unwrapped)
    return False, None

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
    - Uses __all__ to decide public API when available.
    - Pydantic classes: render a Fields table, hide methods.
    - Deduplicates re-exported functions across submodules.
    - Method headings use 'name()' for GitBook RHS nav.
    - Full signature is shown in a Python block.
    - Omits empty sections.
    """
    lines: list[str] = []

    if inspect.isclass(obj):
        # keep current behavior for single class pages (e.g. MLModel)
        if add_top_title:
            lines.append(f"# {obj.__name__}\n")
            desc = _class_description(obj)
            if desc:
                lines.append(desc + "\n")

        if _is_pydantic_model(obj):
            # Only fields for pydantic classes (cleaner output)
            lines.extend(_render_pydantic_fields_for_class(obj))
            return "\n".join(lines)

        # Non-pydantic: show methods
        method_blocks: list[str] = []
        for mname, member in inspect.getmembers(obj):
            if not include_private and mname.startswith("_"):
                continue
            if not inspect.isroutine(member):
                continue
            if getattr(member, "__module__", "").startswith("builtins") or inspect.isbuiltin(member):
                continue
            # Skip deprecated methods globally
            is_dep, _ = _deprecation_info(member)
            if is_dep:
                continue
            if not include_inherited:
                qn = getattr(member, "__qualname__", "")
                if qn.split(".")[0] != obj.__name__:
                    continue
            doc = inspect.getdoc(member) or "_No description available._"
            sig_str = _format_signature(member)
            method_blocks.append(f"### {mname}()\n")
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

        exports = set(getattr(obj, "__all__", []) or [])
        def is_exported(name: str) -> bool:
            return (name in exports) if exports else (not name.startswith("_"))

        # Walk package to collect symbols
        classes: dict[str, type] = {}
        modules = [obj]
        pkg_path = getattr(obj, "__path__", None)
        if pkg_path:
            for _, modname, _ in pkgutil.walk_packages(pkg_path, prefix=obj.__name__ + "."):
                try:
                    mod = importlib.import_module(modname)
                    modules.append(mod)
                except Exception:
                    continue

        # Collect classes exposed by this package
        for mod in modules:
            for cname, cls in inspect.getmembers(mod, inspect.isclass):
                if not is_exported(cname):
                    continue
                if not getattr(cls, "__module__", "").startswith(obj.__name__):
                    continue
                classes[cname] = cls

        # Render classes (alphabetical)
        for cname in sorted(classes):
            cls = classes[cname]
            section: list[str] = [f"## {cname}\n"]
            desc = _class_description(cls)

            # Keep Types clean (as before)
            if getattr(obj, "__name__", "") == "mlserver.types" and _is_pydantic_model(cls):
                pass
            else:
                if desc:
                    section.append(desc + "\n")

            if _is_pydantic_model(cls):
                if _should_include_fields_for_module(obj):
                    fields_lines = _render_pydantic_fields_for_class(cls)
                    if fields_lines:
                        section.extend(fields_lines)
                if _should_include_schema_for_module(obj):
                    section.extend(_render_json_schema_block(cls))
            else:
                # Methods for non-pydantic classes
                method_blocks: list[str] = []

                # In Codecs: include inherited methods and don’t rely on module __all__ for member filtering
                include_inherited_here = _is_codecs_module(obj)

                for mname, member in inspect.getmembers(cls):
                    if not include_private and mname.startswith("_"):
                        continue
                    if not inspect.isroutine(member):
                        continue
                    if getattr(member, "__module__", "").startswith("builtins") or inspect.isbuiltin(member):
                        continue
                    # Skip deprecated methods globally
                    is_dep, _ = _deprecation_info(member)
                    if is_dep:
                        continue
                    # Outside Codecs, only show methods declared on this class
                    if not include_inherited_here:
                        qn = getattr(member, "__qualname__", "")
                        if qn.split(".")[0] != cls.__name__:
                            continue

                    # Docstring: for Codecs, look up through MRO to avoid “No description available.”
                    if include_inherited_here:
                        doc = _get_method_doc_from_mro(cls, mname, member)
                    else:
                        doc = inspect.getdoc(member)

                    sig_str = _format_signature(member)
                    method_blocks.append(f"### {mname}()\n")
                    method_blocks.append(f"```python\n{sig_str}\n```\n")
                    if doc:  # In Codecs, omit placeholder if missing
                        method_blocks.append(f"{doc}\n")

                if method_blocks:
                    section.append("### Methods\n")
                    section.extend(method_blocks)

            lines.append("\n".join(section))

        # Collect standalone functions (dedup across submodules)
        seen_funcs: set[str] = set()
        func_blocks: list[str] = []
        for mod in modules:
            for fname, func in inspect.getmembers(mod, inspect.isfunction):
                if not is_exported(fname):
                    continue
                if not getattr(func, "__module__", "").startswith(obj.__name__):
                    continue
                fqname = f"{func.__module__}.{fname}"
                if fqname in seen_funcs:
                    continue
                # Skip deprecated functions globally
                is_dep, _ = _deprecation_info(func)
                if is_dep:
                    continue
                seen_funcs.add(fqname)
                doc = inspect.getdoc(func) or "_No description available._"
                sig_str = _format_signature(func)
                func_blocks.append(f"## {fname}()\n")
                func_blocks.append(f"```python\n{sig_str}\n```\n")
                func_blocks.append(f"{doc}\n")
        if func_blocks:
            lines.extend(func_blocks)

        return "\n".join(lines)

    raise TypeError(f"Object {obj} is not a class or module")

# ---------------------------
# MLServer CLI (Click) docs
# ---------------------------
def _find_click_root(module: ModuleType):
    """
    Locate the Click root command for mlserver.cli, even if defined in a submodule.
    Preference order:
      1) Group named 'mlserver'
      2) CommandCollection
      3) Any Group
      4) Any Command
    Also checks common attribute names: cli, main, app.
    """
    if not click:
        return None

    candidates: list[click.core.BaseCommand] = []

    def collect_from(mod: ModuleType):
        # Common attributes
        for attr in ("mlserver", "cli", "main", "app"):
            obj = getattr(mod, attr, None)
            if isinstance(obj, (click.core.Command, click.core.Group, click.core.CommandCollection)):  # type: ignore[attr-defined]
                candidates.append(obj)
        # Any commands defined in the module
        for _, obj in inspect.getmembers(mod):
            if isinstance(obj, (click.core.Command, click.core.Group, click.core.CommandCollection)):  # type: ignore[attr-defined]
                candidates.append(obj)

    # Add module and submodules
    collect_from(module)
    pkg_path = getattr(module, "__path__", None)
    if pkg_path:
        for _, subname, _ in pkgutil.walk_packages(pkg_path, prefix=module.__name__ + "."):
            try:
                submod = importlib.import_module(subname)
                collect_from(submod)
            except Exception:
                continue

    # Rank candidates
    def score(cmd: click.core.BaseCommand) -> int:
        # Highest if group named 'mlserver'
        if isinstance(cmd, click.core.Group) and (getattr(cmd, "name", "") == "mlserver"):
            return 100
        # CommandCollection next
        if isinstance(cmd, getattr(click.core, "CommandCollection", tuple())):
            return 90
        # Any Group
        if isinstance(cmd, click.core.Group):
            return 80
        # Any Command
        if isinstance(cmd, click.core.Command):
            return 70
        return 0

    if not candidates:
        return None
    candidates.sort(key=score, reverse=True)
    return candidates[0]

def _click_param_type_name(param_type) -> str:
    try:
        # Click types usually have 'name'
        tname = getattr(param_type, "name", None)
        if tname:
            return tname
        return type(param_type).__name__
    except Exception:
        return "value"

def _render_click_usage(cmd: "click.core.BaseCommand", prog: str) -> str:
    # e.g., mlserver [OPTIONS] COMMAND [ARGS]...
    try:
        parts = [prog]
        if cmd.params:
            parts.append("[OPTIONS]")
        if isinstance(cmd, click.core.Group):
            parts.append("COMMAND [ARGS]...")
        else:
            # Arguments for leaf commands
            for p in cmd.params:
                if isinstance(p, click.core.Argument):
                    name = (p.metavar or p.name or "ARG").upper()
                    parts.append(name if p.required else f"[{name}]")
        return " ".join(parts)
    except Exception:
        return f"{prog} [OPTIONS]"

def _render_click_option(opt: "click.core.Option") -> list[str]:
    # Flags
    flags = list(opt.opts) + list(opt.secondary_opts)
    fallback = f"--{opt.name.replace('_','-')}"
    flags_str = ", ".join(f"`{f}`" for f in flags) if flags else f"`{fallback}`"

    # Metavar/type
    metavar = opt.metavar
    if not metavar and not opt.is_flag:
        metavar = f"<{_click_param_type_name(opt.type)}>"
    head = f"{flags_str}" + (f" `{metavar}`" if metavar else "")

    # Required/default/choices/env
    details = []
    if getattr(opt, "required", False):
        details.append("Required")
    if getattr(opt.type, "choices", None):
        choices = " | ".join(f"`{c}`" for c in opt.type.choices)
        details.append(f"Options: {choices}")
    if opt.default not in (None, (), []):
        details.append(f"Default: `{opt.default}`")
    if opt.envvar:
        if isinstance(opt.envvar, (list, tuple)):
            envs = ", ".join(f"`{e}`" for e in opt.envvar)
        else:
            envs = f"`{opt.envvar}`"
        details.append(f"Env: {envs}")
    suffix = f" ({'; '.join(details)})" if details else ""

    # Help text
    help_text = (opt.help or "").strip()
    return [f"- {head}{suffix}", f"  {help_text}" if help_text else ""]

def _render_click_argument(arg: "click.core.Argument") -> list[str]:
    name = (arg.metavar or arg.name or "ARG").upper()
    req = "Required argument" if arg.required else "Optional argument"
    return [f"- `{name}`", f"  {req}"]

def _render_click_deprecation(help_text: str | None) -> str | None:
    if not help_text:
        return None
    for line in help_text.splitlines():
        if re.search(r"\bdeprecated\b", line, re.IGNORECASE):
            return f"> {line.strip()}"
    return None

def _render_click_command(cmd: "click.core.BaseCommand", prog: str) -> list[str]:
    lines: list[str] = []
    title = cmd.name or prog
    lines.append(f"## {title}\n")

    # Description/help
    help_text = (cmd.help or "").strip()
    dep_note = _render_click_deprecation(help_text)
    if help_text:
        lines.append(f"{help_text}\n")
    if dep_note:
        lines.append(f"{dep_note}\n")

    # Usage
    usage = _render_click_usage(cmd, prog)
    lines.append("```bash")
    lines.append(usage)
    lines.append("```\n")

    # Options and arguments
    options: list[list[str]] = []
    arguments: list[list[str]] = []
    for p in cmd.params or []:
        if isinstance(p, click.core.Option):
            options.append(_render_click_option(p))
        elif isinstance(p, click.core.Argument):
            arguments.append(_render_click_argument(p))
    if options:
        lines.append("### Options\n")
        for block in options:
            for l in block:
                if l:
                    lines.append(l)
            lines.append("")
    if arguments:
        lines.append("### Arguments\n")
        for block in arguments:
            for l in block:
                if l:
                    lines.append(l)
            lines.append("")

    # Subcommands (for Group)
    if isinstance(cmd, click.core.Group):
        subcmds = sorted(cmd.commands.items(), key=lambda kv: kv[0])
        for subname, sub in subcmds:
            # Render subcommand
            lines.extend(_render_click_command(sub, f"{prog} {subname}"))
    return lines

def generate_cli_docs() -> str | None:
    try:
        mod = importlib.import_module("mlserver.cli")
    except Exception:
        return None
    root = _find_click_root(mod)
    if not root:
        return None
    lines: list[str] = []
    lines.append("# MLServer CLI\n")
    lines.append(
        "The MLServer package includes a mlserver CLI designed to help with common tasks in a model’s lifecycle. "
        "You can see a high-level outline at any time via:\n"
    )
    lines.append("```bash")
    lines.append("mlserver --help")
    lines.append("```\n")
    # Render root (mlserver) and all subcommands
    lines.extend(_render_click_command(root, root.name or "mlserver"))
    return "\n".join(lines)

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
            f.write(f"# {name}\n\n")
            if getattr(obj, "__doc__", None):
                f.write(inspect.cleandoc(obj.__doc__) + "\n\n")

            if is_pydantic:
                f.write(document_pydantic_model(obj, source_path) + "\n")
            else:
                content = document_class_or_module(obj, add_top_title=False)
                if content.strip():
                    f.write(content + "\n")

    # Generate CLI docs as a separate page (if click and mlserver.cli are available)
    cli_md = generate_cli_docs()
    if cli_md:
        with open(os.path.join(outdir, "CLI.md"), "w") as f:
            f.write(cli_md)

    print("Docs generated in docs-gb/api/")

if __name__ == "__main__":
    main()
