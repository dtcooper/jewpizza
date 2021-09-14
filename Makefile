.PHONY: build frontend-build lint format pre-commit shell frontend-shell \
	show-outdated copy-js-vendor-deps deploy

COMPOSE=docker compose

build:
	@$(COMPOSE) build --pull

frontend-build:
	@$(COMPOSE) run --rm frontend-dev npm run build

lint:
	@$(COMPOSE) run --rm --no-deps app flake8 || exit 0

format:
	@$(COMPOSE) run --rm --no-deps app sh -c 'black . && isort .' || exit 0

pre-commit: frontend-build format lint

shell:
	@$(COMPOSE) run --rm app bash

frontend-shell:
	@$(COMPOSE) run --rm frontend-dev ash

show-outdated:
	@echo 'Showing outdated dependencies... (empty for none)'
	@echo '============== Frontend =============='
	@$(COMPOSE) run --rm frontend-dev npm outdated
	@echo '============== Backend ==============='
	@$(COMPOSE) run --rm --no-deps app poetry show -o

copy-js-vendor-deps:
	@$(COMPOSE) run --rm frontend-dev ./copy_vendor_deps.sh

deploy:
	git push && ssh jew.pizza 'cd jew.pizza; git pull --ff-only && docker compose build && docker compose up -d'
