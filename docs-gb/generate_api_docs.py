import sys
import json
import inspect
import importlib
from pathlib import Path

# -------------------------------------------------------------------
# Setup paths
# -------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path.cwd() / "docs-gb" / "api-reference" 
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Ensure repo root is importables
sys.path.insert(0, str(REPO_ROOT))

# -------------------------------------------------------------------
# Section mapping (manual control over structure)
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
def iter_public_members(module):
    """Yield (name, object) for public members of a module."""
    for name, obj in inspect.getmembers(module):
        if name.startswith("_"):
            continue
        yield name, obj


def format_signature(obj):
    """Return a string function/class signature if available."""
    try:
        return str(inspect.signature(obj))
    except (TypeError, ValueError):
        return "()"


def document_object(name, obj):
    """Return Markdown documentation for a given class or function."""
    from pydantic import BaseModel

    if inspect.isclass(obj):
        title = f"### Class `{name}`"
        sig = f"class {name}"
        doc = inspect.getdoc(obj) or ""
        md = f"{title}\n\n```python\n{sig}\n```\n\n{doc}\n\n"

        # If it's a Pydantic model, add JSON Schema
        try:
            if issubclass(obj, BaseModel):
                if hasattr(obj, "model_json_schema"):  # Pydantic v2
                    schema = obj.model_json_schema()
                else:  # Pydantic v1
                    schema = obj.schema()

                schema_str = json.dumps(schema, indent=2)
                md += f"**JSON Schema:**\n\n```json\n{schema_str}\n```\n\n"
        except Exception:
            # ignore if not subclassable or schema fails
            pass

        return md

    elif inspect.isfunction(obj):
        title = f"### Function `{name}`"
        sig = format_signature(obj)
        doc = inspect.getdoc(obj) or ""
        return f"{title}\n\n```python\n{name}{sig}\n```\n\n{doc}\n\n"

    return ""


def document_module(module_name):
    """Generate Markdown docs for a single module."""
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        return f"⚠️ Could not import `{module_name}` (missing dependency?): {e}\n\n"
    except Exception as e:
        return f"⚠️ Could not import `{module_name}`: {e}\n\n"

    docs = []
    for name, obj in iter_public_members(module):
        docs.append(document_object(name, obj))
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
