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
copyright = "2021, Seldon Technologies"
html_title = "MLServer"
author = "Seldon Technologies"

# The full version, including alpha/beta/rc tags
release = "0.4.0.dev1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #  "sphinx.ext.autodoc",
    # Creates .nojekyll config
    #  "sphinx.ext.githubpages",
    # Converts markdown to rst
    "myst_parser",
    #  "sphinx.ext.napoleon",
    # automatically generate API docs
    # see https://github.com/rtfd/readthedocs.org/issues/1139
    #  "sphinxcontrib.apidoc",
    "sphinx_search.extension",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# apidoc settings
apidoc_module_dir = "../mlserver"
apidoc_output_dir = "api"
apidoc_excluded_paths = ["**/*test*"]
apidoc_module_first = True
apidoc_separate_modules = True
apidoc_extra_args = ["-d 6"]

# mock imports
autodoc_mock_imports = [
    "pandas",
    "sklearn",
    "skimage",
    "requests",
    "cv2",
    "bs4",
    "keras",
    "seaborn",
    "PIL",
    "tensorflow",
    "spacy",
    "numpy",
    "tensorflow_probability",
    "scipy",
    "matplotlib",
    "creme",
    "cloudpickle",
    "fbprophet",
    "dask",
    "transformers",
]


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = False


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
        "globaltoc_depth": 2,
        "globaltoc_collapse": False,
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
