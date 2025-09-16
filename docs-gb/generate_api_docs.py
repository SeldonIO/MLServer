# import sys
# import json
# import inspect
# import importlib
# from pathlib import Path
# from typing import Any

# # -------------------------------------------------------------------
# # Setup paths
# # -------------------------------------------------------------------
# REPO_ROOT = Path(__file__).resolve().parent.parent
# OUTPUT_DIR = Path.cwd() / "docs-gb" / "api-reference"
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# # Ensure repo root is importable
# sys.path.insert(0, str(REPO_ROOT))

# # -------------------------------------------------------------------
# # Section mapping
# # -------------------------------------------------------------------
# SECTIONS = {
#     "MLServer Settings": ["mlserver.settings"],
#     "Model Settings": ["mlserver.model"],
#     "MLServer CLI": ["mlserver.cli"],
#     "Python API": ["mlserver"],
#     "MLModel": ["mlserver.models"],
#     "Types": ["mlserver.types"],
#     "Codecs": ["mlserver.codecs"],
#     "Metrics": ["mlserver.metrics"],
# }

# # -------------------------------------------------------------------
# # Helpers
# # -------------------------------------------------------------------
# def iter_public_members(module):
#     """Yield (name, object) for public members of a module."""
#     for name, obj in inspect.getmembers(module):
#         if name.startswith("_"):
#             continue
#         yield name, obj


# def format_signature(obj):
#     """Return a string function/class signature if available."""
#     try:
#         return str(inspect.signature(obj))
#     except (TypeError, ValueError):
#         return "()"


# def document_pydantic_model(obj):
#     """Return Markdown for Pydantic models, showing only user-facing fields."""
#     from pydantic import BaseModel, Field

#     md = ""
#     if not issubclass(obj, BaseModel):
#         return md

#     md += "| Field | Type | Default | Description |\n"
#     md += "|-------|------|---------|-------------|\n"

#     for field_name, field_info in obj.model_fields.items():
#         # Skip internal/private fields
#         if field_name.startswith("_"):
#             continue

#         # Field type
#         field_type = getattr(field_info.annotation, "__name__", str(field_info.annotation))

#         # Default
#         default = field_info.default if field_info.default is not None else "-"
#         if callable(default):
#             default = "<callable>"

#         # Description
#         description = field_info.field_info.description or "-"

#         md += f"| `{field_name}` | {field_type} | {default} | {description} |\n"

#     return md + "\n"


# def document_object(name, obj):
#     """Return Markdown documentation for a class or function."""
#     from pydantic import BaseModel

#     if inspect.isclass(obj):
#         title = f"### Class `{name}`"
#         sig = f"class {name}"
#         doc = inspect.getdoc(obj) or ""
#         md = f"{title}\n\n```python\n{sig}\n```\n\n{doc}\n\n"

#         # If it's a Pydantic model, show fields in table format
#         try:
#             if issubclass(obj, BaseModel):
#                 md += document_pydantic_model(obj)
#         except Exception:
#             pass

#         return md

#     elif inspect.isfunction(obj):
#         title = f"### Function `{name}`"
#         sig = format_signature(obj)
#         doc = inspect.getdoc(obj) or ""
#         return f"{title}\n\n```python\n{name}{sig}\n```\n\n{doc}\n\n"

#     return ""


# def document_module(module_name):
#     """Generate Markdown docs for a single module."""
#     try:
#         module = importlib.import_module(module_name)
#     except ImportError as e:
#         return f"⚠️ Could not import `{module_name}` (missing dependency?): {e}\n\n"
#     except Exception as e:
#         return f"⚠️ Could not import `{module_name}`: {e}\n\n"

#     docs = []
#     for name, obj in iter_public_members(module):
#         docs.append(document_object(name, obj))
#     return "\n".join(filter(None, docs))


# # -------------------------------------------------------------------
# # Main entrypoint
# # -------------------------------------------------------------------
# def main():
#     for section, modules in SECTIONS.items():
#         filename = OUTPUT_DIR / f"{section.replace(' ', '_').lower()}.md"
#         out = []
#         out.append(f"# {section}\n")

#         for mod in modules:
#             out.append(f"## Module `{mod}`\n")
#             out.append(document_module(mod))

#         filename.write_text("\n".join(out))
#         print(f"✅ Wrote {filename}")


# if __name__ == "__main__":
#     main()


import sys
import json
import inspect
import importlib
from pathlib import Path
import ast

# -------------------------------------------------------------------
# Setup paths
# -------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path.cwd() / "docs-gb" / "api-reference"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(REPO_ROOT))

# -------------------------------------------------------------------
# Section mapping
# -------------------------------------------------------------------
SECTIONS = {
    "MLServer Settings": ["mlserver.settings"],
    "Model Settings": ["mlserver.model"],
    "MLServer CLI": ["mlserver.cli"],
    "Python API": ["mlserver"],
    "MLModel": ["mlserver.models"],
    "Types": ["mlserver.types"],
    "Codecs": ["mlserver.codecs"],
    "Metrics": ["mlserver.metrics"],
}

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def iter_ast_members(module_path):
    """Return (name, ast_node) for top-level classes/functions in a module."""
    try:
        source = Path(module_path).read_text()
    except FileNotFoundError:
        return []

    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                yield node.name, node
                

def format_signature_from_ast(node: ast.AST) -> str:
    """Return a rough signature from an AST node (function only)."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")
        return f"({', '.join(args)})"
    return "()"

def document_object(name, obj_node, module_name=None):
    """Return Markdown documentation for a class/function AST node."""
    from pydantic import BaseModel

    md = ""
    if isinstance(obj_node, ast.ClassDef):
        # Try to import the class if it's a Pydantic model
        cls = None
        if module_name:
            try:
                module = importlib.import_module(module_name)
                cls = getattr(module, name)
            except Exception:
                cls = None

        title = f"### Class `{name}`"
        md += f"{title}\n\n```python\nclass {name}\n```\n\n"
        doc = ast.get_docstring(obj_node) or ""
        md += f"{doc}\n\n"

        if cls:
            try:
                if issubclass(cls, BaseModel):
                    schema = cls.model_json_schema()
                    schema_str = json.dumps(schema, indent=2)
                    md += f"**JSON Schema:**\n\n```json\n{schema_str}\n```\n\n"
            except Exception:
                pass

    elif isinstance(obj_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        title = f"### Function `{name}`"
        sig = format_signature_from_ast(obj_node)
        doc = ast.get_docstring(obj_node) or ""
        md += f"{title}\n\n```python\n{name}{sig}\n```\n\n{doc}\n\n"

    return md


def document_module(module_name):
    """Generate Markdown docs for a module using AST (only imports BaseModel classes)."""
    try:
        module = importlib.import_module(module_name)
        module_file = Path(module.__file__)
    except Exception as e:
        return f"⚠️ Could not import `{module_name}`: {e}\n\n"

    docs = []
    for name, node in iter_ast_members(module_file):
        docs.append(document_object(name, node, module_name=module_name))
    return "\n".join(filter(None, docs))


# -------------------------------------------------------------------
# Main entrypoint
# -------------------------------------------------------------------
def main():
    for section, modules in SECTIONS.items():
        filename = OUTPUT_DIR / f"{section.replace(' ', '_').lower()}.md"
        out = []
        out.append(f"# {section}\n")

        for mod in modules:
            out.append(f"## Module `{mod}`\n")
            out.append(document_module(mod))

        filename.write_text("\n".join(out))
        print(f"✅ Wrote {filename}")


if __name__ == "__main__":
    main()
