.PHONY: clean-pyc run format

clean-pyc:
	fd -I __pycache__ -x rm -rf {}
	fd -I .pyc -x rm -rf {}

run:
	python manage.py runserver

format:
	black --exclude 'migrations'
	isort --skip-glob *migrations*
