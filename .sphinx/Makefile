# Minimal makefile for Sphinx documentation (GitBook optimized)

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= poetry run sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile install-dev gitbook html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build for GitBook (Markdown output)
gitbook:
	$(SPHINXBUILD) -b markdown "$(SOURCEDIR)" "$(BUILDDIR)/markdown" $(SPHINXOPTS) $(O)

# Build HTML documentation
html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Start development server
start:
	poetry run sphinx-autobuild . ./_build/html

# Install development dependencies
install-dev:
	poetry install -C .. --with docs --with all-runtimes --with all-runtimes-dev

# Clean build artifacts
clean:
	rm -rf "$(BUILDDIR)"
	rm -rf api/*.md api/*.rst 