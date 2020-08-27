.PHONY: build
build:
	docker-compose build

.PHONY: rebuild
rebuild:
	docker-compose build --no-cache

.PHONY: run
run:
	docker-compose up -d

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
