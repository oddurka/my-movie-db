# This Makefile requires the following commands to be available:
# * python3.11
# * poetry (installation guide: https://python-poetry.org/docs/#installing-with-the-official-installer)

# For local development
PYTHONPATH=src
export PYTHONPATH


.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update --no-ansi

# Updates the lock file
.PHONY: lock
lock:
	poetry lock --check

# Activate vitual environment
.PHONY: activate
activate:
	poetry shell


# Activate vitual environment
.PHONY: activate
activate:
	poetry shell

.PHONY: run
run:
	python src/main.py
