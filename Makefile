.PHONY: venv install pre-commit clean
VENV_PYTHON = backend/.venv/bin/python3

init:
	$(MAKE) clean
	if [ "$(shell which poetry)" = "" ]; then \
		$(MAKE) install-poetry; \
	fi
	$(MAKE) setup-poetry

start:
	cd backend; \
	echo Starting env...; \
	poetry config virtualenvs.in-project true; \
	poetry env use python3.10 && poetry install --sync
	
install-poetry:
	cd backend; \
	echo Installing Poetry...; \
	curl -sSL https://install.python-poetry.org | python3 -; \
	$(eval include ${HOME}/.poetry/env)

setup-poetry:
	cd backend; \
	echo Syncing Dependecies...; \
	poetry config virtualenvs.in-project true; \
	poetry env use python3.10 && poetry install --sync; \
	cd ..;

clean:
	cd backend; \
	echo Cleaning...; \
	rm -rf .venv; \
	rm -rf poetry.lock; \
	rm -rf .pytest_cache; \

test: ${VENV_PYTHON}
	cd backend; \
	echo Testing...; \
	poetry run pytest --cov-report xml:tests/coverage.xml --cov

start-project:
	$(MAKE) setup-poetry; \
	cd frontend; \
	npm start && npm run start-backend