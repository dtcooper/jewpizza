.PHONY: pre-commit build build-no-cache shell show-outdated export-show-fixtures deploy up down ssh

COMPOSE:=docker compose
SERVER:=jew.pizza
SERVER_NODENAME:=jewpizza
SERVER_PROJECT_DIR:=dev.jew.pizza
SHELL:=/bin/bash
SHOW_FIXTURE_MODELS=episode showdate
SHOW_FIXTURE_DIR=backend/shows/fixtures/shows

up:
	@$(COMPOSE) up --remove-orphans $(shell source .env; if [ -z "$$DEBUG" -o "$$DEBUG" = 0 ]; then echo "-d"; fi)

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
	$(COMPOSE) pull
	$(COMPOSE) build --pull --build-arg GIT_REV=$(shell git describe --tags --always --dirty)

build-no-cache:
	$(COMPOSE) pull
	$(COMPOSE) build --no-cache --pull --build-arg GIT_REV=$(shell git describe --tags --always --dirty)

shell:
	@$(COMPOSE) run --rm --service-ports --use-aliases app bash || true

show-outdated:
	@echo 'Showing outdated dependencies... (empty means none)'
	@$(COMPOSE) run --rm --no-deps -e "GITHUB_API_TOKEN=$$GITHUB_API_TOKEN" app sh -c '\
		echo "============ Misc Dependencies =========";\
		../scripts/check-versions.sh;\
		echo "============ Frontend (app) ============";\
		npm --prefix=../frontend outdated;\
		echo "============ Backend (app) =============";\
		poetry show -o'
	@$(COMPOSE) run --rm --no-deps sse sh -c '\
		echo "============ Backend (sse) =============";\
		poetry show -o'

export-show-fixtures:
	@for model in $(SHOW_FIXTURE_MODELS); do \
		echo "Exporting $${model}s..." ; \
		$(COMPOSE) run --rm app ./manage.py dumpdata --indent=2 --format=json --natural-primary --natural-foreign \
			"shows.$${model}" > "$(SHOW_FIXTURE_DIR)/$${model}s.json"; \
	done
# @$(COMPOSE) run --rm app ./manage.py dumpdata --indent=2 --format=json --natural-primary --natural-foreign \
# 	shows.episode > backend/shows/fixtures/shows/episodes.json
# @echo 'Exporting show dates...'
# @$(COMPOSE) run --rm app ./manage.py dumpdata --indent=2 --format=json --natural-primary --natural-foreign \
# 	shows.showdate > backend/shows/fixtures/shows/show_dates.json
#@echo '... fixtures exported!'

deploy:
	@if [ $(shell uname -n) = $(SERVER_NODENAME) ]; then \
		git pull --ff-only && make build && make down && make up; \
	else \
		git push && ssh $(SERVER) 'cd $(SERVER_PROJECT_DIR) && make deploy'; \
	fi

down:
	@$(COMPOSE) down --remove-orphans

ssh: # For me only.
	ssh -R 8888:localhost:8000 jew.pizza
