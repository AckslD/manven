PYTHON         = python3
PIP            = pip3
SOURCE_DIR     = manven
TESTS_DIR      = tests
MIN_COV        = 75

help:
	@echo "clean             Cleans .pyc and built files."
	@echo "test-deps         Installs dependencies for running tests."
	@echo "python-deps       Installs dependencies for using package."
	@echo "tests             Runs the tests."
	@echo "open-cov-report   Generates coverage report and opens it."
	@echo "verify            Verifies the installation."
	@echo "install           Installs the package."
	@echo "examples          Runs the examples."
	@echo "build             Builds the wheel of the package."

clean: _delete_pyc _clear_build

_delete_pyc:
	@find . -name '*.pyc' -delete

lint:
	@${PYTHON} -m flake8 ${SOURCE_DIR} ${TESTS_DIR}

python-deps:
	@${PIP} install -r requirements.txt

test-deps:
	@${PIP} install -r test_requirements.txt

tests:
	@${PYTHON} -m pytest --cov=${SOURCE_DIR} --cov-fail-under=${MIN_COV} tests

open-cov-report:
	@${PYTHON} -m pytest --cov=${SOURCE_DIR} --cov-report=html tests && open htmlcov/index.html


_verified:
	@echo "manven is verified!"

verify: clean test-deps lint tests _verified

install: test-deps
	@${PIP} install -e .

_remove_build:
	@rm -f -r build

_remove_dist:
	@rm -f -r dist

_remove_egg_info:
	@rm -f -r *.egg-info

_clear_build: _remove_build _remove_dist _remove_egg_info

_build:
	@${PYTHON} setup.py bdist_wheel

build: _clear_build _build

.PHONY: clean test-deps python-deps lint tests install verify build open-cov-report
