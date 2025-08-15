from __future__ import annotations
import os, sys

import re
from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath(".."))  # make 'mlserver' importable

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.autodoc_pydantic",  # you're using the contrib variant
]

# --- MyST (helps stability of Markdown output) ---
myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "tasklist"]
myst_heading_anchors = 6  # stable anchors 

# --- Autodoc ---
autodoc_member_order = "bysource"
autodoc_class_signature = "separated"
set_type_checking_flag = True
autodoc_typehints = "description"  # (keep only once)

# --- Pydantic (structure the output as tables/sections) ---
# Model / Settings summaries
autodoc_pydantic_model_show_field_summary = True        # summary table of fields
autodoc_pydantic_model_show_validator_summary = True
autodoc_pydantic_settings_show_json = False             
autodoc_pydantic_model_show_json = False

# Field details after the summary
autodoc_pydantic_field_list_all = True
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_field_show_default = True
autodoc_pydantic_field_show_required = True
autodoc_pydantic_field_show_alias = True

# Hide noisy Config blocks (these often collapse into bullet soup in GitBook)
autodoc_pydantic_model_show_config = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_settings_show_config = False
autodoc_pydantic_settings_show_config_summary = False

# Optional: label headings for easier cross-refs if you use them
# extensions += ["sphinx.ext.autosectionlabel"]
# autosectionlabel_prefix_document = True

root_doc = "index"


markdown_anchor_sections = True
markdown_anchor_signatures = True


import re
from pathlib import Path

# Use Sphinx's logger (works across versions)
try:
    from sphinx.util import logging as sphinx_logging
    logger = sphinx_logging.getLogger(__name__)
except Exception:  # ultra-old fallback
    import logging
    logger = logging.getLogger(__name__)

# <a id="X"></a> followed by a Markdown heading (#..######)
_ANCHOR_THEN_HEADING = re.compile(
    r'(?m)^\s*<a id="([^"]+)"></a>\s*\n(#{1,6}\s+[^\n]+?)(\s*\{#.*?\})?\s*$'
)

def _attach_ids_to_headings(app, exception):
    # Only run if build succeeded
    if exception is not None:
        return

    # Only for markdown-style builders (add more names if needed)
    builder_name = getattr(app.builder, "name", "")
    if builder_name not in {"markdown", "md", "mystmd"}:
        logger.info(f"[postprocess] skipping builder '{builder_name}'")
        return

    outdir = Path(app.outdir)
    changed = 0

    for md_path in outdir.rglob("*.md"):
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"[postprocess] skipping {md_path}: {e}")
            continue

        def repl(m):
            anchor_id, heading, explicit = m.group(1), m.group(2), m.group(3)
            return f"{heading}{explicit or f' {{#{anchor_id}}}'}"

        new_text = _ANCHOR_THEN_HEADING.sub(repl, text)
        if new_text != text:
            md_path.write_text(new_text, encoding="utf-8")
            changed += 1

    logger.info(f"[postprocess] normalized anchors in {changed} Markdown files")

def setup(app):
    app.connect("build-finished", _attach_ids_to_headings)
