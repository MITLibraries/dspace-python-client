.PHONY: coveralls install lint sphinx test update bandit black flake isort mypy pydocstyle

help: ## Print this message
	@awk 'BEGIN { FS = ":.*##"; print "Usage:  make <target>\n\nTargets:" } \
/^[-_[:alpha:]]+:.?*##/ { printf "  %-15s%s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build:
	rm -r dist
	poetry build

coveralls: test
	poetry run coveralls

install: ## Install dependencies, including dev dependencies
	poetry install

lint: bandit black flake isort mypy pydocstyle ## Runs all linters

test: ## Run tests
	poetry run pytest --cov=dspace

sphinx: ## Build docs with Sphinx
	poetry run $(MAKE) -C docs clean
	poetry run sphinx-apidoc -f -o docs/source/ dspace
	poetry run $(MAKE) -C docs html

update: ## Update all Python dependencies
	poetry update


## Individual linter commands

bandit: ## Security oriented static analyser for python code
	poetry run bandit -r dspace

black: ## The Uncompromising Code Formatter
	poetry run black --check --diff .

flake: ## Tool For Style Guide Enforcement
	poetry run flake8 .

isort: ## isort your imports, so you don't have to
	poetry run isort . --diff

mypy: ## Static type checker for Python 3 and Python 2.7
	poetry run mypy .

pydocstyle: ## Static analysis tool for checking compliance with Python docstring conventions
	poetry run pydocstyle --convention google --add-ignore=D105,D107 dspace
