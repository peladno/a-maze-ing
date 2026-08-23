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
	poetry run python3 a_maze_ing.py config.txt

debug:
	poetry run python3 -m pdb a_maze_ing.py config.txt

build:
	poetry build --output .

clean:
	rm -rf dist/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/

clean-cache:
	poetry cache clear --all

.PHONY: install test lint lint-strict run debug build clean clean-cache
