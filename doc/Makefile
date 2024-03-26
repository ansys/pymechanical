# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    = -j auto
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
	@echo "Generating LaTeX files from documentation source..."
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "LaTeX files generated successfully."

	@echo "Changing directory to LaTeX build directory..."
	@cd $(BUILDDIR)/latex && \
	echo "Current directory: $(PWD)" && \
	echo "Listing files in directory:" && \
	ls -l && \
	echo "Running latexmk to compile LaTeX files..." && \
	latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	@echo "LaTeX compilation completed."

	@echo "Checking for existence of PDF files..."
	@(test -f $(BUILDDIR)/latex/*.pdf && echo "PDF files exist.") || (echo "No PDF files found."; exit 1)
	@echo "PDF generation successful."