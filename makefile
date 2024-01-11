
py = python manage.py

pip:
	@echo "setup packages manager..."
	pip install --upgrade pip 
	pip install pip-tools
	
install-deps:
	@echo "Installing dependecies packages"
	pip-sync dev-requirements.txt

copy-envs:
	@echo "Copying environment variables.."
	cp contrib/env-sample .env

migrations:
	@echo "Setting migrations"
	$(py) makemigrations
	$(py) migrate

build:
	@echo "Starting initial setup"
	@make pip
	@make install-deps
	@make copy-envs
	@make migrations

up:
	$(py) runserver

compile:
	pip-compile -o requirements.txt pyproject.toml
	pip-compile --extra=dev --output-file=dev-requirements.txt pyproject.toml

back-formatter:
	@echo "Formatting code accord Pep8 Style..."

	@echo "Sorting Imports..."
	isort --force-alphabetical-sort-within-sections .

	@echo "Formatting code..."
	black .

	@echo "Running flake8"
	flake8

	@echo "Completed with 0 erros"

test:
	pytest --tb=short -s --cov
	@make back-formatter

flush:
	@echo "Reseting DATABASE..."
	$(py) reset_db --noinput --close-sessions
	@make migrations

dump:
	$(py) dumpdata auth users.user --natural-primary --natural-foreign > utils/fixtures.json

load:
	@make flush
	$(py) loaddata utils/fixtures.json

