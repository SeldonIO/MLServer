# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import sphinx_material

project = "MLServer"
copyright = "2023, Seldon Technologies"
html_title = "MLServer Documentation"
author = "Seldon Technologies"

# The full version, including alpha/beta/rc tags
release = "1.5.0.dev1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx_search.extension",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_click",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Pydantic settings
autodoc_pydantic_settings_show_json = False

# Bibtex settings
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"

# Auto-generate header anchors
myst_heading_anchors = 3


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# Chosen Themes:
# * https://github.com/bashtage/sphinx-material/
# * https://github.com/myyasuda/sphinx_materialdesign_theme
html_theme = "sphinx_material"

if html_theme == "sphinx_material":
    html_theme_options = {
        "google_analytics_account": "",
        "base_url": "https://mlserver.readthedocs.io",
        "color_primary": "teal",
        "color_accent": "light-blue",
        "repo_url": "https://github.com/SeldonIO/MLServer/",
        "repo_name": "MLServer",
        "globaltoc_depth": 4,
        "globaltoc_collapse": True,
        "globaltoc_includehidden": True,
        "repo_type": "github",
        "nav_links": [
            {
                "href": "https://docs.seldon.io",
                "internal": False,
                "title": "🚀 Our Other Projects & Products:",
            },
            {
                "href": "https://docs.seldon.io/projects/seldon-core/en/latest/",
                "internal": False,
                "title": "Seldon Core",
            },
            {
                "href": "https://docs.seldon.io/projects/alibi/en/stable/",
                "internal": False,
                "title": "Alibi Explain",
            },
            {
                "href": "https://docs.seldon.io/projects/alibi-detect/en/stable/",
                "internal": False,
                "title": "Alibi Detect",
            },
            {
                "href": "https://tempo.readthedocs.io/en/latest/",
                "internal": False,
                "title": "Tempo SDK",
            },
            {
                "href": "https://deploy.seldon.io/",
                "internal": False,
                "title": "Seldon Deploy (Enterprise)",
            },
            {
                "href": (
                    "https://github.com/SeldonIO/seldon-deploy-sdk#seldon-deploy-sdk"
                ),
                "internal": False,
                "title": "Seldon Deploy SDK (Enterprise)",
            },
        ],
    }

    extensions.append("sphinx_material")
    html_theme_path = sphinx_material.html_theme_path()
    html_context = sphinx_material.get_html_context()

html_favicon = "favicon.ico"
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]
