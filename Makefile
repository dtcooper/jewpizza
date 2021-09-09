.PHONY: frontend-build shell lint format pre-commit

frontend-build:
	@docker-compose run --rm frontend-dev npm run build

lint:
	@docker-compose run --rm --no-deps app flake8 || exit 0

format:
	@docker-compose run --rm --no-deps app sh -c 'black . && isort .' || exit 0

pre-commit: frontend-build format lint

shell:
	@docker-compose run --rm app bash
