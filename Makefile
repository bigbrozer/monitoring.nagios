clean: py-bytecode backup-files

#dochtml:
#	@echo 'Creating HTML documentation...'
#	@(cd doc; $(MAKE) html)
#	@xdg-open doc/build/html/index.html

py-bytecode:
	@echo 'Cleaning Python byte code files...'
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/

backup-files:
	@echo 'Cleaning backup files...'
	@find . -name '*~' -exec rm -f {} +
	@find . -name '#*#' -exec rm -f {} +

#doc-build:
#	@echo 'Cleaning documentation build...'
#	@(cd doc; $(MAKE) clean )
