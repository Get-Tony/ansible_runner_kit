# Tool configured is located in the pyproject.toml file.
# Author: Anthony Pagan <Get-Tony@outlook.com>
# Usage: make [target]

EXCLUDED_DIRS := -path "./venv" -o -path "./env" -o -path "./.venv" -o -path "./.env" -path "./.git" -o -path "./.mypy_cache" -o -path "./.pytest_cache" -o -path "./.coverage" -o -path "./.ruff_cache"
PYTHON_FILES := $(shell find . -type d \( $(EXCLUDED_DIRS) \) -prune -o -type f -name "*.py" -print)
YAML_FILES := $(shell find . -type d \( $(EXCLUDED_DIRS) \) -prune -o -type f \( -name "*.yaml" -o -name "*.yml" \) -print)

all: lint-python lint-yaml checks_passed

lint-python: lint-with-mypy lint-with-black lint-with-pylint lint-with-ruff

lint-yaml: lint-with-ansible

lint-with-mypy:
	@echo "Running mypy..."
	@mypy $(PYTHON_FILES)

lint-with-black:
	@echo "Running black..."
	@black --check $(PYTHON_FILES)

lint-with-pylint:
	@echo "Running pylint..."
	@pylint $(PYTHON_FILES)

lint-with-ruff:
	@echo "Running ruff..."
	@ruff $(PYTHON_FILES)

lint-with-ansible:
	@echo "Running ansible-lint..."
	@ansible-lint $(YAML_FILES)

wipe-cache:
	@echo "Wiping cache..."
	@rm -rf .mypy_cache .pytest_cache .coverage .ruff_cache

checks_passed:
	@echo "All checks passed"

.PHONY: all lint-python lint-yaml lint-with-mypy lint-with-black lint-with-pylint lint-with-ruff lint-with-ansible wipe-cache checks_passed
