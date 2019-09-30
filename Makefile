.PHONY: clean clean-build clean-pyc lint test setup help
SHELL := /bin/bash
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

setup: ## install python project dependencies
	pip install --upgrade pip wheel
	pip install --upgrade -r requirements.txt
	pip install -e .

setup-tests: ## install python project dependencies for tests
	pip install --upgrade pip wheel
	pip install --upgrade -r requirements.test.txt
	pip install -e .
	anyblok_createdb -c app.test.cfg || anyblok_updatedb -c app.test.cfg

init-dev: ## setup python venv for dev purposes, runs it and load tmuxp session
	( \
		source venv/bin/activate || python3 -m venv venv && source venv/bin/activate; \
		make setup-dev && make setup-tests; \
		tmuxp load trainwarner.tmuxp.yml; \
	)

setup-dev: ## install python project dependencies for development
	pip install --upgrade pip wheel
	pip install --upgrade -r requirements.dev.txt
	pip install -e .
	anyblok_createdb -c app.dev.cfg || anyblok_updatedb -c app.dev.cfg
#	## install nodejs / npm
#	nodeenv -p
#	npm i -g npm
#	npm --prefix trainwarner_project/backend_ui/ install

run-dev: ## launch pyramid development server
	anyblok_pyramid -c app.dev.cfg --wsgi-host 0.0.0.0

run-gunicorn: ## launch pyramid server with gunicorn
	gunicorn_anyblok_pyramid --anyblok-configfile app.cfg

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 trainwarner_project/bloks

test: ## run anyblok nose tests
	ANYBLOK_CONFIG_FILE=app.test.cfg py.test --show-progress -ra -vv -s --cov-report term-missing --cov=trainwarner_project -W ignore::DeprecationWarning trainwarner_project/bloks/

documentation: ## generate documentation
	anyblok_doc -c app.test.cfg --doc-format RST --doc-output doc/source/apidoc.rst
	make -C doc/ html
	coverage html -d doc/build/html/coverage

# run-dev-npm: ## launch npm development server with hot reload (Vuejs based Backend UI)
# 	npm --prefix trainwarner_project/backend_ui/ update
# 	npm --prefix trainwarner_project/backend_ui/ run serve
# 
# build-assets: ## build js and scss assets for production
# 	npm --prefix trainwarner_project/backend_ui/ update
# 	npm --prefix trainwarner_project/backend_ui/ run build
# 
# run-dev-npm-frontend: ## launch npm development server with hot reload (Vuejs frontend components)
# 	npm --prefix trainwarner_project/frontend_ui/ update
# 	npm --prefix trainwarner_project/frontend_ui/ run watch
# 
# build-assets-frontend: ## build js and scss assets for production
# 	npm --prefix trainwarner_project/frontend_ui/ update
# 	npm --prefix trainwarner_project/frontend_ui/ run build
# 
# populate-dev: ## populate development database with fake data
# 	anyblok_populate_fake_data -c app.dev.cfg
# 
# populate-test: ## populate test database with fake data
# 	anyblok_populate_fake_data -c app.test.cfg
# 
# locale-extract: ## Extract locale from .py and .jinja2 files and generate files for french translation.
# 	pybabel extract --mapping trainwarner_project/bloks/frontend/babel.cfg --output-file=trainwarner_project/bloks/frontend/locale/messages.pot trainwarner_project/bloks/frontend/
# 	test -f trainwarner_project/bloks/frontend/locale/fr/LC_MESSAGES/messages.po || pybabel init -i trainwarner_project/bloks/frontend/locale/messages.pot -d trainwarner_project/bloks/frontend/locale -l fr
# 	pybabel update --domain=messages -l fr --input-file=trainwarner_project/bloks/frontend/locale/messages.pot --output-dir=trainwarner_project/bloks/frontend/locale
# 
# locale-compile: ## Compile locale files (from .po to .mo)
# 	pybabel compile -d trainwarner_project/bloks/frontend/locale
