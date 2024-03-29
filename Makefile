.PHONY: test version tests build dist release
ifndef VERBOSE
.SILENT:
endif

PACKAGENAME := $(shell poetry version | awk {'print $$1'})

default:
	@echo "Usage:"
	@echo "- make test         | run tests"
	@echo "- make black        | run black -l 120"
	@echo "- make release      | upload dist and push tag"

install:
	poetry install

pytest:
	PYTHONPATH=. poetry run pytest --cov-report term-missing --cov=${PACKAGENAME}/ tests -v

flake8:
	poetry run flake8 ${PACKAGENAME}/ tests/

mypy:
	poetry run mypy ${PACKAGENAME}/

version:
	PYTHONPATH=. poetry run python -m ${PACKAGENAME}.__version__ > /dev/null
	poetry version `PYTHONPATH=. poetry run python -m ${PACKAGENAME}.__version__`

black:
	poetry run black ${PACKAGENAME}/ tests/

isort:
	poetry run isort ${PACKAGENAME}/ tests/

build:
	rm -rf dist/
	poetry build

release:
	make install
	make pytest
	make flake8
	make mypy
	make version
	make build
	twine upload dist/${PACKAGENAME}-`PYTHONPATH=. poetry run python -m ${PACKAGENAME}.__version__`*
	git add pyproject.toml ${PACKAGENAME}/__version__.py ${PACKAGENAME}/__version_data__.py
	git commit -m "Bumped version" --allow-empty
	git tag -a `PYTHONPATH=. poetry run python -m ${PACKAGENAME}.__version__` -m `PYTHONPATH=. poetry run python -m ${PACKAGENAME}.__version__`
	git push
	git push --tags

test: pytest flake8 mypy
tests: test
dist: build
lint: flake8 mypy
pylint: flake8 mypy
