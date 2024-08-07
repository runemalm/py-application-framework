##########################################################################
# This is the project's Makefile.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################

HOME := $(shell echo ~)
PWD := $(shell pwd)
SRC := $(PWD)/src
EXAMPLES := $(PWD)/examples
TESTS := $(PWD)/tests
DOCS := $(PWD)/docs

# Load env file
include env.make
export $(shell sed 's/=.*//' env.make)

##########################################################################
# MENU
##########################################################################

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##########################################################################
# TEST
##########################################################################

.PHONY: test
test: ## run test suite
	PYTHONPATH=$(SRC):$(TESTS) pipenv run pytest $(TESTS)

################################################################################
# RELEASE
################################################################################

.PHONY: build
build: ## build the python package
	pipenv run python setup.py sdist bdist_wheel

.PHONY: clean
clean: ## clean the build
	python setup.py clean
	rm -rf build dist
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

.PHONY: upload-test
upload-test: ## upload package to testpypi repository
	TWINE_USERNAME=$(PYPI_USERNAME_TEST) TWINE_PASSWORD=$(PYPI_PASSWORD_TEST) pipenv run twine upload --repository testpypi --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## upload package to pypi repository
	TWINE_USERNAME=$(PYPI_USERNAME) TWINE_PASSWORD=$(PYPI_PASSWORD) pipenv run twine upload --skip-existing dist/*

.PHONY: sphinx-quickstart
sphinx-quickstart: ## run the sphinx quickstart
	docker run -it --rm -v $(PWD)/docs:/docs sphinxdoc/sphinx sphinx-quickstart

.PHONY: sphinx-html
sphinx-html: ## build the sphinx html
	make -C docs html

.PHONY: sphinx-rebuild
sphinx-rebuild: ## re-build the sphinx docs
	cd $(DOCS) && \
	pipenv run make clean && pipenv run make html

.PHONY: sphinx-autobuild
sphinx-autobuild: ## activate autobuild of docs
	cd $(DOCS) && \
	pipenv run sphinx-autobuild . _build/html --watch $(SRC)

################################################################################
# CLI
################################################################################

.PHONY: cli-venv-create
cli-venv-create: ## setup the cli virtual environment
	python -m venv venv_cli

.PHONY: cli-uninstall-editable
cli-uninstall-editable: ## uninstall the tool from the virtual environment
	source venv_cli/bin/activate && \
	pip uninstall -y py-application-framework

.PHONY: cli-install-editable
cli-install-editable: ## install the tool in the virtual environment
	source venv_cli/bin/activate && \
	pip uninstall -y py-application-framework && \
	pip install -e .

.PHONY: cli-run
cli-run: ## run the cli tool
	source venv_cli/bin/activate && \
	application_framework --help

################################################################################
# PIPENV
################################################################################

.PHONY: pipenv-install
pipenv-install: ## setup the virtual environment
	pipenv --python 3.7 install --dev

.PHONY: pipenv-install-package
pipenv-install-package: ## install a package (uses PACKAGE)
	pipenv install $(PACKAGE)

.PHONY: pipenv-install-package-dev
pipenv-install-package-dev: ## install a dev package (uses PACKAGE)
	pipenv install --dev $(PACKAGE)

.PHONY: pipenv-packages-graph
pipenv-packages-graph: ## Check installed packages
	pipenv graph

.PHONY: pipenv-requirements-generate
pipenv-requirements-generate: ## Check a requirements.txt
	pipenv lock -r > requirements.txt

.PHONY: pipenv-shell
pipenv-shell: ## Activate the virtual environment
	pipenv shell

.PHONY: pipenv-venv
pipenv-venv: ## Show the path to the venv
	pipenv --venv

.PHONY: pipenv-lock-and-install
pipenv-lock-and-install: ## Lock the pipfile and install (after updating Pipfile)
	pipenv lock && \
	pipenv install --dev

.PHONY: pipenv-pip-freeze
pipenv-pip-freeze: ## Run pip freeze in the virtual environment
	pipenv run pip freeze

.PHONY: pipenv-setup-sync
pipenv-setup-sync: ## Sync dependencies between Pipfile and setup.py
	pipenv run pipenv-setup sync

################################################################################
# EXAMPLES
################################################################################

.PHONY: examples-single-app-run
examples-single-app-run: ## run the single-app example
	cd $(EXAMPLES)/single_app && PYTHONPATH=$(SRC):$(PWD) pipenv run python main.py
# 	PYTHONPATH=$(SRC):$(PWD) pipenv run python $(EXAMPLES)/single_app/main.py
