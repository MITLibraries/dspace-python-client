.PHONY: coveralls install lint test update bandit black flake isort

help: ## Print this message
	@awk 'BEGIN { FS = ":.*##"; print "Usage:  make <target>\n\nTargets:" } \
/^[-_[:alpha:]]+:.?*##/ { printf "  %-15s%s\n", $$1, $$2 }' $(MAKEFILE_LIST)

coveralls: test
	poetry run coveralls

install: ## Install dependencies, including dev dependencies
	poetry install

lint: bandit black flake isort ## Runs all linters

test: ## Run tests
	poetry run pytest --cov=dspace

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
