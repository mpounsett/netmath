# Netmath

A native python library for doing network math

## Testing

You will need (at least) python 2.7, 3.4, 3.5, 3.6, and 3.7.  The easiest way
to get these all installed is with
[pyenv](https://www.holger-peters.de/using-pyenv-and-tox.html).  As of last
update, the current versions are:

```
pyenv install 2.7.16
pyenv install 3.4.10
pyenv install 3.5.7
pyenv install 3.6.9
pyenv install 3.7.4
pyenv global 3.7.4 3.6.5 3.5.5 3.4.8 2.7.15 system
```

Before running tests you will require some python packages to be installed.

```
pip install -r requirements_test.txt
```

To run all tests:

```
tox
```
