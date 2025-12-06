# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

html:
	@echo "Building HTML into ../docs (repo root)..."
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "../docs" $(SPHINXOPTS)
	@touch ../docs/.nojekyll
	@echo "Build finished. The HTML pages are in ../docs"

# Clean target that removes the generated files in the repo root
clean:
	@echo "Cleaning up generated HTML and doctree files..."
	@rm -rf ../docs
	@echo "Clean complete."

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
