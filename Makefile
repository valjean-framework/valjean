#init:
#	pip install -r requirements.txt

test:
	py.test -v tests

.PHONY: test
#.PHONY: init test
