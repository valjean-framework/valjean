install-deps:
	pip install -r requirements.txt

test:
	py.test tests

html:
	cd doc && $(MAKE) html

.PHONY: install-deps test html
