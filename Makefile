.PHONY: clean dist distclean

all: clean dist

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	rm -Rf build rndc.egg-info __pycache__

distclean: clean
	rm -Rf dist

dist:
	python setup.py bdist_wheel
	python setup.py sdist
