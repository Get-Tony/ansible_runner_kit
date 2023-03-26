install:
	./setup_environment.sh

dev:
	./setup_environment.sh --dev

format:
	black .

lint:
	black . --check
	ruff .
	mypy .
	pylint playbook_manager.py --output-format=colorized

check: format lint

clean:
	rm -rf .pytest_cache .mypy_cache .coverage .ruff_cache
