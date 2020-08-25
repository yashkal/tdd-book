.PHONY: clean-pyc run format

dc-build:
	docker-compose build

dc-rebuild:
	docker-compose build --no-cache

dc-up:
	docker-compose up -d

dc-down:
	docker-compose down

clean-pyc:
	fd -I __pycache__ -x rm -rf {}
	fd -I .pyc -x rm -rf {}

run:
	python manage.py runserver

format:
	black --exclude 'migrations'
	isort --skip-glob *migrations*
