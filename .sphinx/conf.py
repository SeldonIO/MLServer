import pathlib, sys
# Make repo root importable (so "import mlserver" works)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

project = "MLServer"
extensions = [
    "myst_parser",              # allow Markdown in Sphinx
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",      # Google/Numpy docstrings
]

# Generate autosummary pages from our hub automatically
autosummary_generate = True
autosummary_generate_overwrite = True
autodoc_member_order = "bysource"

# Mock heavy/optional deps so imports never break at build time
autodoc_mock_imports = [
    "pydantic", "pydantic_settings", "starlette", "fastapi",
    "tritonclient", "aiohttp", "torch", "sklearn", "xgboost",
    "lightgbm", "catboost", "pandas", "numpy", "uvicorn", "grpc",
]

# Add the Markdown builder if present (so RTD—or other envs—don’t fail)
try:
    import sphinx_markdown_builder  # noqa: F401
    extensions.append("sphinx_markdown_builder")
except Exception:
    pass

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# shorter titles 
add_module_names = False

# keep logical grouping or follow source order (pick one)
autodoc_member_order = "bysource"   # or "groupwise"
