.PHONY: run build

CONTAINER=jew-pizza-site

run:
	docker run -it --rm -p 8000:8000 -v "$(CURDIR):/app" "$(CONTAINER)" sh -c 'poetry run bash'

build:
	docker build -t "$(CONTAINER)" .
