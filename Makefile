VENV = $(shell readlink -f ./venv)
HOST_PYTHON ?= python3

export PYTHON = $(VENV)/bin/python3
export PIP = $(VENV)/bin/pip
export PYTEST = $(VENV)/bin/pytest

test: test-deps
ifdef TESTS
	$(PYTEST) -v -k "$(TESTS)"
else
	$(PYTEST) -v
endif

deps: .requirements.upvest.flag
test-deps: .requirements.upvest.flag .requirements.test.flag

.requirements.%.flag: requirements.%.txt | $(VENV)
	$(PIP) install -r $<
	touch $@

$(VENV):
	$(HOST_PYTHON) -m venv $@

clean:
	rm -rf $(VENV) .*.flag

.PHONY: test deps
