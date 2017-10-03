install-deps:
	pip install -r requirements.txt

test:
	py.test -v -s --hypothesis-show-statistics tests

html:
	cd doc && $(MAKE) html

.PHONY: install-deps test html
