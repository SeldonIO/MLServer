from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(".."))  # so 'mlserver' imports

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.autodoc_pydantic",        
]

# MyST
myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "tasklist"]

# Optional: add stable anchors on headings (GitBook likes these)
myst_heading_anchors = 3   # add anchors to h1..h3



# Autodoc defaults (can be overridden per block)
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,          # include members by default
    "undoc-members": True,    # include undoc'd members if present
    "show-inheritance": True,
}

# Type hints and forward refs
set_type_checking_flag = True
autodoc_typehints = "description"
typehints_fully_qualified = True
autodoc_class_signature = "separated"   # cleaner class signatures

root_doc = "index"

autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = True
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_model_show_field_summary = True

autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_config = False
autodoc_pydantic_model_show_validator_summary = True
autodoc_pydantic_field_list_all = True

autodoc_typehints = "description"   # or "signature"/"none"

# --- autodoc_pydantic: prefer structured sections/tables over inline blobs ---
# Expand field details after the summary:
autodoc_pydantic_field_show_default = True
autodoc_pydantic_field_show_required = True
autodoc_pydantic_field_show_alias = True

# Reduce noisy "Config" blocks that GitBook often squashes into bullets:
autodoc_pydantic_settings_show_config = False
autodoc_pydantic_settings_show_config_summary = False

# Optional: better cross-refs to sections (adds labels for every heading)
autosectionlabel_prefix_document = True

