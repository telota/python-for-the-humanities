.DEFAULT_GOAL := build

.PHONY: clean
clean:
	rm -R site

.PHONY: build
build:
	./generate-docs.py
	mkdocs build

.PHONY: deploy
deploy: clean build
	git diff --quiet || git commit -a -m "Updates generated contents."
	mkdocs gh-deploy
