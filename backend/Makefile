.PHONY: venv install pre-commit clean
VENV_PYTHON = .venv/bin/python3

init: 
	@$(MAKE) clean
	@if [ "$(shell which poetry)" = "" ]; then \
		$(MAKE) install-poetry; \
	fi
	@$(MAKE) setup-poetry

install-poetry:
	@echo Installing Poetry...
	@curl -sSL https://install.python-poetry.org | python3 -
	@$(eval include ${HOME}/.poetry/env)

setup-poetry:
	@echo Installing Dependecies...
	@poetry config virtualenvs.in-project true
	@poetry env use python3.10 && poetry install --sync

clean:
	@echo Cleaning...
	rm -rf .venv
	rm -rf poetry.lock
	rm -rf .pytest_cache

test: ${VENV_PYTHON}
	@echo Testing...
	@poetry run pytest --cov-report xml:tests/coverage.xml --cov