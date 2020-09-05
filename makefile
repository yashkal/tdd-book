.PHONY: build
build:
	docker-compose build

.PHONY: rebuild
rebuild:
	docker-compose build --no-cache

.PHONY: run
run:
	docker-compose up -d

.PHONY: test utest ftest
test: utest ftest ## Run all tests

utest: export DEBUG=1
utest: export DJANGO_ALLOWED_HOSTS=localhost
utest: export SECRET_KEY=foo
utest: ## Run unit tests
	pytest -v --override-ini DJANGO_SETTINGS_MODULE=superlists.settings --ignore=app/functional_tests app

ftest: ## Run functional tests
	pytest -v app/functional_tests

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
