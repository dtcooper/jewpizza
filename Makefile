.PHONY: pre-commit build shell show-outdated deploy up down

COMPOSE:=docker compose
SERVER:=jew.pizza
SERVER_PROJET_DIR:=jew.pizza

pre-commit:
	@$(COMPOSE) run --rm --no-deps app sh -c '\
		echo "============== djlint ================";\
		djlint --reformat . ;\
		echo "============== standard ==============";\
		npx --prefix=/app/frontend standard --fix ;\
		echo "============== black =================";\
		black . ;\
		echo "============== isort =================";\
		isort . ;\
		echo "============== flake8 ================";\
		flake8;\
		exit 0'

build:
	@$(COMPOSE) build --pull

shell:
	@$(COMPOSE) run --rm --service-ports app bash

show-outdated:
	@echo 'Showing outdated dependencies... (empty for none)'
	@$(COMPOSE) run --rm --no-deps app sh -c '\
		echo "============== Frontend ==============";\
		npm --prefix=../frontend outdated;\
		echo "============== Backend ===============";\
		poetry show -o'

deploy:
	git push && ssh $(SERVER) 'cd $(SERVER_PROJET_DIR); git pull --ff-only && make build && make up'

up:
	@$(COMPOSE) up $(shell source .env; if [ -z "$$DEBUG" -o "$$DEBUG" = 0 ]; then echo "-d"; fi)

down:
	@$(COMPOSE) down
