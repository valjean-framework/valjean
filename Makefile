all: install-deps html doctest test

install-deps:
	pip install -r requirements.txt

test:
	py.test -v -s --hypothesis-show-statistics tests

doctest:
	cd doc && $(MAKE) doctest

html:
	cd doc && $(MAKE) html

.PHONY: install-deps test html
