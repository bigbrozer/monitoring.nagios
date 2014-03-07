default:

clean: py-bytecode backup-files

doc: clean-doc
	@echo 'Creating HTML documentation...'
	@(cd docs; $(MAKE) html)

clean-doc:
	@echo 'Cleaning documentation build...'
	@(cd docs; $(MAKE) clean )

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

.PHONY: default clean doc clean-doc py-bytecode backup-files
