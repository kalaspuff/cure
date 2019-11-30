# `cure`
[![pypi](https://badge.fury.io/py/cure.svg)](https://pypi.python.org/pypi/cure/)
[![Made with Python](https://img.shields.io/pypi/pyversions/cure)](https://www.python.org/)
[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/cure)
[![MIT License](https://img.shields.io/github/license/kalaspuff/cure.svg)](https://github.com/kalaspuff/cure/blob/master/LICENSE)
[![Code coverage](https://codecov.io/gh/kalaspuff/cure/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/cure/tree/master/cure)

*Library for adding trailing underscores to passed down keyword arguments from third party libraries. Adds the preferred trailing underscore to the key in the kwarg if the key would conflict with the Python reserved keywords or Python built-ins. Methods can be decorated with the `@cure` decorator.*


## Installation with `pip`
Like you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.
```
$ pip install cure
```


## Usage and examples

#### `@cure` decorator
