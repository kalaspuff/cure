# `cure`
![Python package](https://github.com/kalaspuff/cure/workflows/Python%20package/badge.svg)
[![pypi](https://badge.fury.io/py/cure.svg)](https://pypi.python.org/pypi/cure/)
[![Made with Python](https://img.shields.io/pypi/pyversions/cure)](https://www.python.org/)
[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/cure)
[![MIT License](https://img.shields.io/github/license/kalaspuff/cure.svg)](https://github.com/kalaspuff/cure/blob/master/LICENSE)
[![Code coverage](https://codecov.io/gh/kalaspuff/cure/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/cure/tree/master/cure)

*Library for adding trailing underscores to passed down keyword arguments from third party libraries. Adds the preferred trailing underscore to the key in the kwarg if the key would conflict with the Python reserved keywords or Python built-ins. Methods can be decorated with the `@cure` decorator.*

Can also be used to convert input keyword arguments to snake case. All in all a decorator to put on your functions which take input from third party libraries which are dependant on user input. In my experience this may happen when working with web frameworks that may apply query values as kwargs or when interfacing with GraphQL libraries that will send user input arguments as kwargs.

As described in *PEP 8 -- Style Guide for Python Code* (https://www.python.org/dev/peps/pep-0008/):
> The following special forms using leading or trailing underscores are recognized (these can generally be combined with any case convention):
>
> `single_trailing_underscore_`: used by convention to avoid conflicts with Python keyword.


## Installation with `pip`
Like you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.
```
$ pip install cure
```


## Usage and examples

#### Use the `@cure.decorator`

```python
import cure

@cure.decorator(cure.KEYWORD_TRAILING_UNDERSCORES)
def my_function(id_=None, username=None, type_=None):
    pass
```

This function could then be called with the keyword arguments `id`, `username` and/or `type`. Since `id` and `type` are either reserved Python keywords or are Python built-ins and shouldn't be used as names, the decorator will add a trailing underscore to the kwargs before passing them into our function `my_function`.

#### Convert kwargs to snake case as well

```python
import cure

@cure.decorator(cure.KEYWORD_TRAILING_UNDERSCORES | cure.KEYWORD_SNAKE_CASE_RECURSIVE)
def graphql_resolver(obj, info, resource_id, type_=None):
    pass
```

This function uses both the options of adding trailing underscores to reserved keywords and built-ins as well as the option of converting input kwargs to snake case. Let's say we're dealing with a GraphQL framework which would otherwise call our function like this, depending on the user input `my_function(None, info, resourceId=kwargs["resourceId"], type=kwargs["type"])` or even more likely like `my_function(None, info, **kwargs)` where `kwargs` would be a dict holding the keys `resourceId` and `type`. Since we want our code to be Pythonic and adhere to proper naming conventions the `@cure.decorator` can help out with removing the hurdle of converting the kwargs ourself or by jumping through hoops otherwise required.

#### Available options
* `cure.KEYWORD_TRAILING_UNDERSCORES`: Adds trailing underscores to keys in keyword arguments that are using a name that is either a reserved keyword or a Python built-in.
* `cure.KEYWORD_SNAKE_CASE`: Converts keys in keyword arguments to snake case.
* `cure.KEYWORD_SNAKE_CASE_RECURSIVE`: Converts keys in keyword arguments to snake case. If the keyword argument's value is a dict or a list of dicts it will also convert keys within these to snake case.
* `cure.KEYWORD_CAMEL_CASE`: Converts keys in keyword arguments to camel case. This is not recommended, but may be used as a reversal of values converted by the snake case decorator.
* `cure.KEYWORD_CAMEL_CASE_RECURSIVE`: Recursive conversion to camel case.

#### Other functions
The following functions are also available from the module.

##### `cure.is_keyword(kw)`
```python
import cure

cure.is_keyword("id")
# True
cure.is_keyword("type")
# True
cure.is_keyword("api")
# False
```

##### `cure.trail_name(kw)`
```python
import cure

cure.trail_name("id")
# "id_"
cure.trail_name("type")
# "type_"
cure.trail_name("api")
# "api"
```

##### `cure.snake_case_name(kw)` and `cure.snake_case_dict(input_dict, recursive)`
```python
import cure

cure.snake_case_name("apiSecret")
# "api_secret"
cure.snake_case_dict({"user": {"userId": 4711, "userLevel": "ADMIN"}}, recursive=True)
# {'user': {'user_id': 4711, 'user_level': 'ADMIN'}}
```

##### `cure.camel_case_name(kw)` and `cure.camel_case_dict(input_dict, recursive)`
```python
import cure

cure.camel_case_name("api_secret")
# "apiSecret"
cure.camel_case_dict({"user": {"user_id": 4711, "user_level": "ADMIN"}}, recursive=True)
# {'user': {'userId': 4711, 'userLevel': 'ADMIN'}}
```
