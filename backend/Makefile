.PHONY: venv install pre-commit clean
PYTHON = $(shell python -c 'import sys; print(sys.executable)')
VENV_PYTHON = .venv/Scripts/python.exe

init: clean venv install

venv: $(PYTHON)
	@echo Creating .venv...
	virtualenv -V || pip install virtualenv
	$(PYTHON) -m venv .venv
	poetry -V || ${VENV_PYTHON} -m pip install --upgrade pip wheel setuptools poetry

install: ${VENV_PYTHON}
	@echo Installing dependencies...
	poetry install --no-root --remove-untracked

clean:
	@echo Cleaning...
	if exist .\\.venv\\ ( rmdir .\\.venv /q /s )
	if exist poetry.lock ( del poetry.lock /q /s )
	if exist .pytest_cache ( rmdir .pytest_cache /q /s )

test: ${VENV_PYTHON}
	@echo Testing...
	poetry run pytest