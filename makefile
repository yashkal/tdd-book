export SECRET_KEY = django_testing # Must be set for pytest-django to run

.PHONY: help
help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build/rebuild container images
	docker-compose build --no-cache

.PHONY: run
run: ## Start running containers
	docker-compose up -d

.PHONY: test utest ftest
test: ## Run unit and function tests (`utest` and `ftest` targets)
	pytest app

utest:
	pytest --ignore=app/functional_tests app

ftest:
	pytest app/functional_tests

.PHONY: logs
logs: ## View container log files
	docker-compose logs

.PHONY: clean clean-pyc
clean: ## Stop and remove containers
	docker-compose down --remove-orphans

clean-pyc: ## Remove pycache
	fd -I __pycache__ app -x rm -rvf {}
	fd -I .pyc app -x rm -rvf {}
	fd --hidden .pytest_cache app -x rm -rvf

.PHONY: format
format: ## Format python code
	black --exclude 'migrations' app
	isort --skip-glob *migrations* app
