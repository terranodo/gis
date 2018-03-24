help:
	@echo "Usage:"
	@echo "    make help        show this message"
	@echo "    make setup       create virtual environment and install dependencies"
	@echo "    make activate    enter virtual environment"
	@echo "    make test        run the test suite"
	@echo "    exit             leave virtual environment"

setup:
	pip install pipenv
	pipenv install --dev --three

activate:
	pipenv shell -c

test:
	pipenv run python test.py

coverage:
	pipenv run -- coverage run --source=gis test.py

flake:
	pipenv run flake8

release: coverage flake
	pipenv run python setup.py sdist upload --repository=https://upload.pypi.org/legacy/

send_coverage:
	pipenv run python -c "from coveralls.cli import main;print(main());"

.PHONY: help setup activate test coverage flake release send_coverage
