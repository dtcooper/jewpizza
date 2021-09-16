.PHONY: lint format pre-commit shell show-outdated deploy

COMPOSE=docker compose

lint:
	@$(COMPOSE) run --rm --no-deps app flake8 || exit 0

format:
	@$(COMPOSE) run --rm --no-deps app sh -c 'black . && isort .' || exit 0

pre-commit: format lint

shell:
	@$(COMPOSE) run --rm app bash

show-outdated:
	@echo 'Showing outdated dependencies... (empty for none)'
	@$(COMPOSE) run --rm --no-deps app sh -c '\
		echo "============== Frontend ==============";\
		npm --prefix=../frontend outdated; \
		echo "============== Backend ==============="; \
		poetry show -o'

deploy:
	git push && ssh jew.pizza 'cd jew.pizza; git pull --ff-only && docker compose build && docker compose up -d'
