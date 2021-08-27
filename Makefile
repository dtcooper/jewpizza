.PHONY: run required-built build

CONTAINER=jew-pizza-site

run: required-built
	docker run -it --rm -p 8000:8000 -v "$(CURDIR):/app" "$(CONTAINER)" sh -c 'poetry run bash'

required-built:
	@[ "$$(docker images -q $(CONTAINER))" = "" ] && docker build -t $(CONTAINER) . || exit 0

build:
	docker build -t "$(CONTAINER)" .
