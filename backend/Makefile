.PHONY: venv install pre-commit clean
PYTHON = $(shell python -c 'import sys; print(sys.executable)')
VENV_PYTHON = .venv/Scripts/python.exe

init: clean venv install

venv: $(PYTHON)
	@echo "Creating .venv..."
	virtualenv -V || pip install virtualenv
	$(PYTHON) -m venv .venv
	poetry -V || pip install --upgrade pip wheel setuptools poetry

install: ${VENV_PYTHON}
	@echo "Installing dependencies..."
	poetry install --no-root --remove-untracked

clean:
	@echo "Cleaning..."
	if exist .\\.venv\\ ( rmdir .\\.venv /q /s )
	if exist poetry.lock ( del poetry.lock /q /s )

test:
	@echo "Testing..."
	${VENV_PYTHON} ./tests/test_placeholder.py