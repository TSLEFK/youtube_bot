###############
# Tests
###############

test:
	poetry run python -m pytest
test-ci:
	poetry run python -m pytest --cov-report=xml
test-no-cov:
	poetry run python -m pytest --no-cov

###############
# CDK
###############

cdk-ls-dev:
	poetry run npx cdk ls -c env=dev
cdk-ls-prd:
	poetry run npx cdk ls -c env=prd
cdk-ls-all:
	@make cdk-ls-dev
	@make cdk-ls-prd

###############
# setups
###############

freeze:
	poetry run python -m pip freeze

setup:
	@make setup-poetry
	@make setup-poetry-dev

setup-poetry:
	python -m pip install -U --no-cache-dir poetry
setup-poetry-dev:
	poetry install --no-interaction

###############
# Docker Compose Contents
###############

up:
	docker compose up --build -d ${SERVICE}
build:
	docker compose build --no-cache --force-rm
ps:
	docker compose ps -a
stop:
	docker compose stop ${SERVICE}
down:
	docker compose down --remove-orphans
destroy:
	cd tests_medium && docker compose down --rmi all --volumes --remove-orphans
logs:
	docker compose logs ${SERVICE}
restart:
	@make down
	@make up
	@make ps
remake:
	@make destroy
	@make build
	@make up