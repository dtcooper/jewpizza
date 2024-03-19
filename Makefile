COMPOSE:=docker compose
SHELL:=/bin/bash

.PHONY: up
up: CONTAINERS:=
up: .env
	$(COMPOSE) up --remove-orphans $(shell source .env; if [ -z "$$DEV_MODE" -o "$$DEV_MODE" = 0 ]; then echo "-d"; fi) $(CONTAINERS)

.PHONY: down
down:
	$(COMPOSE) down --remove-orphans

.PHONY: shell
shell: CONTAINER:=backend
shell:
	$(COMPOSE) run --service-ports --use-aliases --rm $(CONTAINER) /bin/bash

.PHONY: build
build: CONTAINERS:=
build:
	$(COMPOSE) build $(CONTAINERS)
