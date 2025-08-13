# MLServer Sphinx Documentation (GitBook Optimized)

This directory contains the Sphinx configuration for building MLServer documentation that is optimized for GitBook deployment.

## Overview

This setup follows the same approach as the main `docs/` folder but is specifically configured for:

- **Sphinx + GitBook compatibility**: Outputs Markdown that works well with GitBook
- **API documentation**: Auto-generated from the MLServer Python code
- **Clean structure**: Organized documentation following the main docs approach

## Structure

```
.sphinx/
├── conf.py              # Sphinx configuration
├── index.md             # Main documentation index
├── api/                 # API documentation
│   ├── reference.md     # API overview
│   ├── model.md         # MLModel documentation
│   ├── codecs.md        # Codecs documentation
│   ├── types.md         # Types documentation
│   └── metrics.md       # Metrics documentation
├── _static/             # Static assets
│   └── css/
│       └── custom.css   # Custom styling
├── Makefile             # Build commands
└── README.md            # This file
```

## Building Documentation

### Prerequisites

Install the required dependencies:

```bash
make install-dev
```

### Build Commands

- **HTML documentation**: `make html`
- **GitBook Markdown**: `make gitbook`
- **Development server**: `make start`
- **Clean build**: `make clean`

### GitBook Deployment

To build for GitBook deployment:

```bash
make gitbook
```

This will generate Markdown files in `_build/markdown/` that can be used with GitBook.

## Configuration

The `conf.py` file is configured to:

- Use the same extensions as the main docs
- Output Markdown for GitBook compatibility
- Auto-generate API documentation using autodoc2
- Include proper styling and navigation

## Differences from Main Docs

This setup differs from the main `docs/` folder in that it:

1. **Focuses on API documentation**: Primarily for reference material
2. **GitBook optimized**: Outputs Markdown instead of HTML
3. **Simplified structure**: Less content, more focused on code reference
4. **Same approach**: Uses the same configuration patterns and extensions

## Customization

To customize the documentation:

1. **Add new API modules**: Update `autodoc2_packages` in `conf.py`
2. **Modify styling**: Edit `_static/css/custom.css`
3. **Add content**: Create new `.md` files and update the toctree
4. **Change theme**: Modify `html_theme_options` in `conf.py` 