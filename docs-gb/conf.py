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

root_doc = "index"

autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = True
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_model_show_field_summary = True

autodoc_typehints = "description"   # or "signature"/"none"