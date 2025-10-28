# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    = -j auto -v
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
LINKCHECKDIR  = $(BUILDDIR)/linkcheck

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# customized clean due to examples gallery
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf source/examples/gallery_examples
	find . -type d -name "_autosummary" -exec rm -rf {} +

# customized clean due to examples gallery
clean-except-examples:
	rm -rf $(BUILDDIR)/*
	rm -rf images/auto-generated
	find . -type d -name "_autosummary" -exec rm -rf {} +

# customized to build the pdf rather than using latexpdf due to various issues
# with our docs like GIFs being written as PNG.
pdf:
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd $(BUILDDIR)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f $(BUILDDIR)/latex/*.pdf && echo pdf exists) || exit 1

# generate docs without examples
html-noplot:
	@$(SPHINXBUILD) -D plot_gallery=0 -b html $(SOURCEDIR) $(BUILDDIR)/html $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."