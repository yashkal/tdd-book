.PHONY: build
build:
	docker-compose build

.PHONY: rebuild
rebuild:
	docker-compose build --no-cache

.PHONY: run
run:
	docker-compose up -d

.PHONY: test
test: export DEBUG=1
test: export DJANGO_ALLOWED_HOSTS=localhost
test: export SECRET_KEY=foo
test:
	pytest -v app

.PHONY: logs
logs:
	docker-compose logs

.PHONY: clean
clean: 
	docker-compose down --remove-orphans

.PHONY: clean-pyc
clean-pyc:
	fd -I __pycache__ -x rm -rf {}
	fd -I .pyc -x rm -rf {}

.PHONY: format
format:
	black --exclude 'migrations'
	isort --skip-glob *migrations* app
