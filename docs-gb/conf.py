from __future__ import annotations
import os, sys
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
myst_heading_anchors = 3   # stable anchors on h1..h3 for GitBook

# --- Autodoc ---
autodoc_member_order = "bysource"
autodoc_class_signature = "separated"
set_type_checking_flag = True
autodoc_typehints = "description"  # (keep only once)

# --- Pydantic (structure the output as tables/sections) ---
# Model / Settings summaries
autodoc_pydantic_model_show_field_summary = True        # summary table of fields
autodoc_pydantic_model_show_validator_summary = True
autodoc_pydantic_settings_show_json = True              # JSON example for Settings (optional)
autodoc_pydantic_model_show_json = True                 # JSON example for Models (optional)

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
