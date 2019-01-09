# Makefile for Sphinx documentation
#

# You can set these variables from the command line.

# Turn warnings into errors. NOTE: do not remove this flag! Sphinx is very
# permissive when it comes to errors, and generally will not fail when an
# extension raises one, so this flag is mission-critical. All custom directives
# now raise a `docutils`-based exception, which Sphinx will convert to a.
# warning. Without this flag, that warning will never see the light of day.
SPHINXOPTS    = -W
SPHINXBUILD   = sphinx-build
BUILDDIR      = build
DEBUG         =

# Internal variables.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) source

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean      to remove previous builds"
	@echo "  html       to build production-ready docs"
	@echo "  preview    to build a preview of the docs without running any commands (DO NOT DEPLOY PREVIEW BUILDS)"
	@echo "  preview DEBUG=relative/path-no-ext                                     (runs commands for that page)"
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
	$(SPHINXBUILD) -b dirhtml -D command_block_no_exec=1 -D debug_page=$(DEBUG) $(ALLSPHINXOPTS) $(BUILDDIR)/preview
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

.PHONY: deploy-workshop-s3
deploy-workshop-s3:
	aws s3 sync \
		--exclude *.DS_Store \
		--acl public-read \
		build/fmt-cdiff-s3/ \
		s3://qiime2-workshops/fmt-cdiff
