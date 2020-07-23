.PHONY: clean-pyc run format

docker-build:
	docker build --tag superlists .

docker-run:
	docker run --rm --name superlists -p 8000:8000 superlists

docker-clean:
	docker rmi superlists

clean-pyc:
	fd -I __pycache__ -x rm -rf {}
	fd -I .pyc -x rm -rf {}

run:
	python manage.py runserver

format:
	black --exclude 'migrations'
	isort --skip-glob *migrations*
