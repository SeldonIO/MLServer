# Make sure imports work from the repo root
import os, sys
sys.path.insert(0, os.path.abspath(".."))

print("CONF LOADED FROM:", __file__)

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.autosummary",
    "sphinx_markdown_builder",
]


source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst",
}

root_doc = "index"

autosummary_generate = True
autosummary_generate_overwrite = True

autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_show_json = False

autosummary_imported_members = False

exclude_patterns = ["_build", ".doctrees", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

myst_heading_anchors = 6

# Templates (adjust if your Jinja lives elsewhere)
templates_path = ["_templates"]

autodoc_mock_imports = ["torch", "tensorflow", "onnxruntime"]

# put the __init__ signature in a separate block (not in the heading)
autodoc_class_signature = "separated"   # default is "mixed"

# move type hints into the description instead of the signature
autodoc_typehints = "description"

# shorten fully-qualified type names (e.g., List[int] instead of typing.List[int])
python_use_unqualified_type_names = True



exclude_patterns = [
    "_build", ".doctrees", "Thumbs.db", ".DS_Store",
    "**/PULL_REQUEST_TEMPLATE/**",  # ignore repo hygiene files
    "**/.github/**",                # if present
]

myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "tasklist"]
myst_heading_anchors = 6


print("CONF: autosummary_generate =", globals().get("autosummary_generate"))
print("CONF: myst_enable_extensions =", globals().get("myst_enable_extensions"))

print("TEMPLATES PATH:", [os.path.abspath(path) for path in templates_path])

