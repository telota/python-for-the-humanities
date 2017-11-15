.DEFAULT_GOAL := build

.PHONY: clean
clean:
	rm -R site

.PHONY: build
build:
	mkdocs build

.PHONY: deploy
deploy: clean build
	mkdocs gh-deploy
