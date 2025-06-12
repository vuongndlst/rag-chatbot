.PHONY: test lint

test:
pytest

lint:
ruff backend

