PYTHON ?= python3
VENV ?= .venv
PIP = $(VENV)/bin/pip
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest

.PHONY: setup install run migrate test lint clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install: setup

run:
	$(FLASK) --app wsgi:app run --host=0.0.0.0 --port=5000

migrate:
	$(VENV)/bin/alembic upgrade head

test:
	$(PYTEST) -q

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ app/__pycache__ tests/__pycache__ *.db
