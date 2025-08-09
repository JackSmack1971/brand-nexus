.PHONY: setup lint fmt typecheck test\:unit test\:all cov build

setup:
	pip install -r requirements-dev.txt

lint:
	ruff check src tests
	black --check src tests

fmt:
	black src tests

typecheck:
	mypy src

test\:unit:
	PYTHONPATH=src pytest tests/unit

test\:all:
	PYTHONPATH=src pytest

cov:
	PYTHONPATH=src pytest --cov=src/brandnexus --cov-report=term-missing --cov-fail-under=70


build:
	python -m build
