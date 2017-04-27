.DEFAULT_GOAL := build

.PHONY: build
build:
	./generate-docs.py
	mkdocs build

.PHONY: deploy
deploy: build
	git diff --quiet || git commit -a -m "Updates generated contents."
	mkdocs gh-deploy
