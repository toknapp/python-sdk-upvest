.PHONY: help clean clean-pyc clean-build lint test coverage publish fmt docs

help:
	@echo "clean - remove build and Python file artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with prospector"
	@echo "fmt - trigger pre-commit code linting and formatting"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "publish - package and upload a release"

init:
	pip install pipenv --upgrade
	pipenv shell --three

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
# pipenv run flake8 --ignore=E501,F401,E128,E402,E731,F821 upvest
	pipenv run prospector

fmt:
	pre-commit run --all-files

test: clean
	pipenv run py.test -s -v

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=upvest tests

publish: clean test
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info

docs:
	@echo "==> Building documentaion"
	@cd docs/; make html

clean-docs:
	@echo "==> Cleaning documentaion"
	@cd docs/; make clean
