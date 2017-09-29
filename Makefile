#init:
#	pip install -r requirements.txt

test:
	py.test tests

.PHONY: test
#.PHONY: init test
