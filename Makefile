VENV = $(shell readlink -f ./venv)
HOST_PYTHON ?= python3

export PYTHON = $(VENV)/bin/python3
export PIP = $(VENV)/bin/pip
export PYTEST = $(VENV)/bin/pytest

test: deps
	$(PYTEST) -v

deps: .requirements.flag

.requirements.flag: requirements.txt | $(VENV)
	$(PIP) install -r $<
	touch $@

$(VENV):
	$(HOST_PYTHON) -m venv $@

clean:
	rm -rf $(VENV) .*.flag

.PHONY: test deps
