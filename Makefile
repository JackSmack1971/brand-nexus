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
	pytest --cov=src --cov-report=term-missing

build:
	python -m build
