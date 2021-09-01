.PHONY: run required build

CONTAINER=jew-pizza-site
DEFAULT_ENV_FILE=.env.default
ENV_FILE=.env
LOCAL_PORT:=7152

run: required
	docker run -it --rm -p "$(LOCAL_PORT):8000" -v "$(CURDIR):/app" --env-file "$(ENV_FILE)" "$(CONTAINER)"

shell: required
	docker run -it --rm -p "$(LOCAL_PORT):8000" -v "$(CURDIR):/app" --env-file "$(ENV_FILE)" "$(CONTAINER)" sh -c 'poetry run bash'

prod: required build stop
	docker run -itd --restart=always -p "127.0.0.1:$(LOCAL_PORT):8000" -v "$(CURDIR)/.env:/app/.env" --env-file "$(ENV_FILE)" --name "$(CONTAINER)" "$(CONTAINER)"

stop:
	docker stop $(CONTAINER) || true
	docker rm $(CONTAINER) || true

required:
	@[ ! -f "$(ENV_FILE)" ] && cp "$(DEFAULT_ENV_FILE)" "$(ENV_FILE)" || exit 0
	@[ "$$(docker images -q $(CONTAINER))" = "" ] && docker build -t $(CONTAINER) . || exit 0

build:
	docker build -t "$(CONTAINER)" .
