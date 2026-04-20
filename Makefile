VENV_PATH = .venv
RUFF = $(VENV_PATH)/bin/ruff
TY = $(VENV_PATH)/bin/ty
COVERAGE = $(VENV_PATH)/bin/coverage
PYTEST = $(VENV_PATH)/bin/pytest
MKDOCS = $(VENV_PATH)/bin/mkdocs

.PHONY: setup setup-docs lint format type-check check test coverage docs docs-build clean

setup:
	uv sync --locked

setup-docs: setup
	uv pip install -r requirements-docs.txt

lint:
	$(RUFF) check pyvenezuela tests
	$(RUFF) format pyvenezuela tests --check

format:
	$(RUFF) format pyvenezuela tests
	$(RUFF) check pyvenezuela tests --fix

type-check:
	$(TY) check pyvenezuela

check: lint type-check

test:
	$(COVERAGE) run -m pytest tests $(ARGS)

coverage: test
	$(COVERAGE) report

docs: setup-docs
	$(MKDOCS) serve

docs-build: setup-docs
	$(MKDOCS) build

clean:
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage .pytest_cache .ruff_cache .ty_cache htmlcov dist build site
