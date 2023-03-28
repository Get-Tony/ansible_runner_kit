# Tool configured is located in the pyproject.toml file.
# Author: Anthony Pagan <Get-Tony@outlook.com>
# Usage: make [target]

EXCLUDED_DIRS := -path "./venv" -o -path "./env" -o -path "./.venv" -o -path "./.env"
PYTHON_FILES := $(shell find . -type d \( $(EXCLUDED_DIRS) \) -prune -o -type f -name "*.py" -print)
YAML_FILES := $(shell find . -type d \( $(EXCLUDED_DIRS) \) -prune -o -type f \( -name "*.yaml" -o -name "*.yml" \) -print)


all: lint-python lint-yaml

lint-python: lint-with-mypy lint-with-black lint-with-pylint lint-with-ruff

lint-yaml: lint-with-ansible

lint-with-mypy:
	mypy --strict $(PYTHON_FILES)

lint-with-black:
	black --check $(PYTHON_FILES)

lint-with-pylint:
	pylint $(PYTHON_FILES)

lint-with-ruff:
	ruff $(PYTHON_FILES)

lint-with-ansible:
	ansible-lint $(YAML_FILES)
