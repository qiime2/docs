# Makefile for Sphinx documentation
#

# You can set these variables from the command line.

# Turn warnings into errors.
SPHINXOPTS    = -W
SPHINXBUILD   = sphinx-build
BUILDDIR      = build

# Internal variables.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) source

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean      to remove previous builds"
	@echo "  html       to build production-ready docs"
	@echo "  preview    to build a preview of the docs without running any commands (DO NOT DEPLOY PREVIEW BUILDS)"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  dummy      to check syntax errors of document sources"

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*

# Disable incremental builds for now until it is safe to use with the
# `command-block` directive:
#     https://github.com/qiime2/qiime2.github.io/issues/28
.PHONY: html
html: clean
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Production build finished. The HTML pages are in $(BUILDDIR)/html."
	@echo
	@echo "Run the following command to view the build locally:"
	@echo
	@echo "cd build/html && python -m http.server ; cd -"

.PHONY: preview
preview: clean
	$(SPHINXBUILD) -b dirhtml -D command_block_no_exec=1 $(ALLSPHINXOPTS) $(BUILDDIR)/preview
	@echo
	@echo "Preview build finished. The HTML pages are in $(BUILDDIR)/preview. DO NOT DEPLOY THIS PREVIEW BUILD."
	@echo
	@echo "Run the following command to view the build locally:"
	@echo
	@echo "cd build/preview && python -m http.server ; cd -"

.PHONY: linkcheck
linkcheck:
	$(SPHINXBUILD) -b linkcheck -D command_block_no_exec=1 $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

.PHONY: dummy
dummy:
	$(SPHINXBUILD) -b dummy -D command_block_no_exec=1 $(ALLSPHINXOPTS) $(BUILDDIR)/dummy
	@echo
	@echo "Build finished. Dummy builder generates no files."
