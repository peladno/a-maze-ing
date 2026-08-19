install:
    poetry install

test:
    poetry run pytest -q

lint:
    poetry run flake8 .
    poetry run mypy . \
        --warn-return-any \
        --warn-unused-ignores \
        --ignore-missing-imports \
        --disallow-untyped-defs \
        --check-untyped-defs

lint-strict:
    poetry run flake8 .
    poetry run mypy . --strict

run:
    poetry run python -m mazegen

clean:
    rm -rf dist/
    rm -rf .mypy_cache/
    rm -rf .pytest_cache/

.PHONY: install test lint lint-strict run clean
