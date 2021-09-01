.PHONY: run required build

CONTAINER=jew-pizza-site
DEFAULT_ENV_FILE=.env.default
ENV_FILE=.env
LOCAL_PORT:=8000

run: required
	docker run -it --rm -p "$(LOCAL_PORT):8000" -v "$(CURDIR):/app" --env-file "$(ENV_FILE)" "$(CONTAINER)"

shell: required
	docker run -it --rm -p "$(LOCAL_PORT):8000" -v "$(CURDIR):/app" --env-file "$(ENV_FILE)" "$(CONTAINER)" sh -c 'poetry run bash'

required:
	@[ ! -f "$(ENV_FILE)" ] && cp "$(DEFAULT_ENV_FILE)" "$(ENV_FILE)" || exit 0
	@[ "$$(docker images -q $(CONTAINER))" = "" ] && docker build -t $(CONTAINER) . || exit 0

build:
	docker build -t "$(CONTAINER)" .
