.PHONY: clean coverage docs help quality requirements selfcheck test test-all upgrade validate

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## remove generated byte code, coverage reports, and build artifacts
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	coverage erase
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

coverage: clean ## generate and view HTML coverage report
	coverage report html
	$(BROWSER) htmlcov/index.html

export CUSTOM_COMPILE_COMMAND = make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -q pip-tools
	pip-compile --upgrade -o requirements/dev.txt requirements/base.in requirements/dev.in requirements/quality.in requirements/test.in requirements/travis.in
	pip-compile --upgrade -o requirements/quality.txt requirements/base.in requirements/quality.in requirements/test.in
	pip-compile --upgrade -o requirements/test.txt requirements/base.in requirements/test.in
	pip-compile --upgrade -o requirements/travis.txt requirements/travis.in
	# Let tox control the Django version for tests
	sed '/django==/d' requirements/test.txt > requirements/test.tmp
	mv requirements/test.tmp requirements/test.txt

quality: ## check coding style with pycodestyle and pylint
	tox -e quality

requirements: ## install development environment requirements
	pip install -qr requirements/dev.txt --exists-action w
	pip-sync requirements/dev.txt requirements/private.*

test: clean ## run tests in the current virtualenv
	python manage.py test

diff_cover: test ## find diff lines that need test coverage
	diff-cover coverage.xml

test-all: ## run tests on every supported Python/Django combination
	tox -e quality
	tox

validate: quality test ## run tests and quality checks

selfcheck: ## check that the Makefile is well-formed
	@echo "The Makefile is well-formed."
