all: install-deps html doctest test

install-deps:
	pip3 install -r requirements.txt

test tests:
	py.test

test-verbose tests-verbose:
	py.test --valjean-verbose

doctest:
	cd doc && $(MAKE) doctest

check: test doctest

html:
	cd doc && $(MAKE) html

lint:
	@flake8

clean:
	cd doc && $(MAKE) clean

.PHONY: all install-deps test tests doctest check html lint clean
