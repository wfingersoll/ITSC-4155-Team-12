PY = python3
VENV = venv
BIN=$(VENV)/bin
ifeq ($(OS), Windows_NT)
    BIN=$(VENV)/Scripts
    PY=python
endif

$(VENV): pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/poetry sync
	touch $(VENV)

clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

test: $(VENV)
	$(BIN)/pip -V
	$(BIN)/python tests/test_placeholder.py