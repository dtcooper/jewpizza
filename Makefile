.PHONY: pre-commit build shell show-outdated deploy up down ssh

COMPOSE:=docker compose
SERVER:=jew.pizza
SERVER_NODENAME:=jewpizza
SERVER_PROJECT_DIR:=dev.jew.pizza
SHELL:=/bin/bash

pre-commit:
	@$(COMPOSE) run --rm --no-deps app sh -c '\
		echo "=============== standard ===============";\
		npx --prefix=/app/frontend standard --fix ;\
		echo "=============== black ==================";\
		black . ;\
		black --config pyproject.toml ../sse ;\
		echo "=============== isort ==================";\
		isort . ;\
		isort --sp pyproject.toml ../sse ;\
		echo "=============== flake8 =================";\
		flake8;\
		flake8 --config .flake8 ../sse ;\
		exit 0'

build:
	@$(COMPOSE) pull
	@$(COMPOSE) build --pull --build-arg GIT_REV=$(shell git describe --tags --always --dirty)

shell:
	@$(COMPOSE) run --rm --service-ports --use-aliases app bash || true

show-outdated:
	@echo 'Showing outdated dependencies... (empty for none)'
	@$(COMPOSE) run --rm --no-deps app sh -c '\
		echo "============ Frontend (app) ============";\
		npm --prefix=../frontend outdated;\
		echo "============ Backend (app) =============";\
		poetry show -o'
	@$(COMPOSE) run --rm --no-deps sse sh -c '\
		echo "============ Backend (sse) =============";\
		poetry show -o'

deploy:
	@if [ $(shell uname -n) = $(SERVER_NODENAME) ]; then \
		git pull --ff-only && make build && make down && make up; \
	else \
		git push && ssh $(SERVER) 'cd $(SERVER_PROJECT_DIR) && make deploy'; \
	fi

up:
	@$(COMPOSE) up --remove-orphans $(shell source .env; if [ -z "$$DEBUG" -o "$$DEBUG" = 0 ]; then echo "-d"; fi)

down:
	@$(COMPOSE) down --remove-orphans

ssh: # For me only.
	ssh -R 8888:localhost:8000 jew.pizza
