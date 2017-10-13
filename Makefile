all: install-deps html doctest test

install-deps:
	pip install -r requirements.txt

test tests:
	py.test -v -s --hypothesis-show-statistics tests

doctest:
	cd doc && $(MAKE) doctest

check: test doctest

html:
	cd doc && $(MAKE) html

clean:
	cd doc && $(MAKE) clean

.PHONY: all install-deps test tests doctest check html clean
