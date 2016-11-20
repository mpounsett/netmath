python=python

build:
	${python} setup.py build

test: build
	${python} test/network_tests.py

install: test
	${python} setup.py install
