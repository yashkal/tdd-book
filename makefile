.PHONY: clean-pyc run

clean-pyc:
	fd -I .pyc -x rm -rf {}
	fd -I __pycache__ -x rm -rf {}

run:
	python manage.py runserver
