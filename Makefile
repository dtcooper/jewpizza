.PHONY: up down pre-commit build build-no-cache shell shell-no-deps show-outdated env-diff export-show-fixtures ssh

COMPOSE:=docker compose
SERVER:=jew.pizza
SERVER_NODENAME:=jewpizza
SERVER_PROJECT_DIR:=dev.jew.pizza
SHELL:=/bin/bash
SHOW_FIXTURE_MODELS=episode showdate
SHOW_FIXTURE_DIR=backend/shows/fixtures/shows
GIT_REV=$(shell git describe --tags --always --abbrev=8 --dirty)
BUILD_DATE=$(shell date -u +%FT%TZ)

up: CONTAINERS:=
up:
	$(COMPOSE) up --remove-orphans $(shell source .env; if [ -z "$$DEBUG" -o "$$DEBUG" = 0 ]; then echo "-d"; fi) $(CONTAINERS)

down:
	$(COMPOSE) down --remove-orphans

pre-commit:
	@APP_IP_OVERRIDE=172.22.0.50 $(COMPOSE) run --rm --no-deps app sh -c '\
		echo "=============== black ==================";\
		black . ;\
		echo "=============== isort ==================";\
		isort . ;\
		echo "=============== flake8 =================";\
		flake8;\
		echo "=============== standard ===============";\
		cd ../frontend/src ;\
		npx standard --fix ;\
		exit 0'

build: CONTAINERS:=
build:
	$(COMPOSE) build --pull --build-arg GIT_REV=$(GIT_REV) --build-arg BUILD_DATE=$(BUILD_DATE) $(CONTAINERS)

build-no-cache: CONTAINERS:=
build-no-cache:
	$(COMPOSE) build --no-cache --pull --build-arg GIT_REV=$(GIT_REV) --build-arg BUILD_DATE=$(BUILD_DATE) $(CONTAINERS)

shell: CONTAINER:=app
shell:
	@APP_IP_OVERRIDE=172.22.0.51 $(COMPOSE) run --rm --service-ports --use-aliases -e "GITHUB_API_TOKEN=$$GITHUB_API_TOKEN" $(CONTAINER) $$([ "$(CONTAINER)" = radio ] && echo /bin/bash || echo /bin/ash) || true

shell-no-deps: CONTAINER:=app
shell-no-deps:
	@APP_IP_OVERRIDE=172.22.0.52 $(COMPOSE) run --rm --no-deps --service-ports -e "GITHUB_API_TOKEN=$$GITHUB_API_TOKEN" $(CONTAINER) $$([ "$(CONTAINER)" = radio ] && echo /bin/bash || echo /bin/ash) || true

show-outdated:
	@echo 'Showing outdated dependencies... (empty means none)'
	@APP_IP_OVERRIDE=172.22.0.53 $(COMPOSE) run --rm --no-deps -e "GITHUB_API_TOKEN=$$GITHUB_API_TOKEN" -e NO_STARTUP_MESSAGE=1 app sh -c '\
		echo "============ Misc Dependencies =========";\
		../scripts/check-versions.sh;\
		echo "============ Frontend (app) ============";\
		npm --prefix=../frontend outdated;\
		echo "============ Backend (app) =============";\
		poetry show -o'

export-show-fixtures:
	@for model in $(SHOW_FIXTURE_MODELS); do \
		echo "Exporting $${model}s..." ; \
		APP_IP_OVERRIDE=172.22.0.54 $(COMPOSE) run --rm app ./manage.py dumpdata --indent=2 --format=json --natural-primary --natural-foreign \
			"shows.$${model}" > "$(SHOW_FIXTURE_DIR)/$${model}s.json" ; \
		bzip2 -9f "$(SHOW_FIXTURE_DIR)/$${model}s.json" ; \
	done

env-diff:
	@APP_IP_OVERRIDE=172.22.0.55 $(COMPOSE) run -v "$(CURDIR):/mnt" --rm --no-deps -e NO_STARTUP_MESSAGE=1 app sh -c '\
		cd /mnt ; \
		for env in .env .env.sample ; \
			do sed "s/^\([A-Z_]\+\)=.*/\1/" "$$env" > "/tmp/env-$${env}" ; \
		done ; \
		diff --color -u /tmp/env-.env.sample /tmp/env-.env ; \
		rm /tmp/env-.env.sample /tmp/env-.env'

ssh: # For me only.
	ssh -R 8888:localhost:8000 jew.pizza
