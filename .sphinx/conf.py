import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

# -- Project information -----------------------------------------------------
project = "MLServer"
copyright = "2024, Seldon Technologies"
html_title = "MLServer Documentation"
author = "Seldon Technologies"

# The full version, including alpha/beta/rc tags
release = "1.7.0.dev0"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx_markdown_builder",  # for GitBook Markdown output
    "autodoc2",
    "sphinx_search.extension",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_click",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx_copybutton",
]

# Tell autodoc2 what to analyze
autodoc2_packages = [
    {"path": "../mlserver", "module": "mlserver", "auto_mode": False}  # repo-root relative
]

# Skip the problematic file
autodoc2_skip_module_regexes = [r"^mlserver\.settings$"]

# Write files here (relative to .sphinx/)
autodoc2_output_dir = "api"

# Emit Markdown (MyST) instead of RST
autodoc2_render_plugin = "myst"

# Trim the noise (you can dial this back later)
autodoc2_hidden_objects = ["inherited", "private", "dunder"]  # hide inherited/underscored
autodoc2_docstrings = "direct"        # don't pull inherited docstrings
autodoc2_class_docstring = "merge"    # merge __init__ into class doc, don't duplicate
autodoc2_module_summary = False       # drop per-module summary table if you don't want it

# Pydantic settings
autodoc_pydantic_settings_show_json = False

# Auto-generate header anchors
myst_heading_anchors = 3

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# For GitBook, we'll use a simple theme that works well with Markdown
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

html_favicon = "../docs/favicon.ico"
html_sidebars = {
    "**": ["globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Add any paths that contain custom static files
html_static_path = ["_static"]

# -- Options for Markdown output (GitBook) ----------------------------------
# Configure markdown builder for GitBook compatibility
markdown_theme = "gitbook"
markdown_theme_options = {
    "primary_color": "teal",
    "accent_color": "light-blue",
    "repo_url": "https://github.com/SeldonIO/MLServer/",
    "repo_name": "MLServer",
    "globaltoc_depth": 4,
    "globaltoc_collapse": True,
    "globaltoc_includehidden": True,
}
