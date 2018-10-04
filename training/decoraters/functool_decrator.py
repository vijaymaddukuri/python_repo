"""
When we use the decorator, function name and docstring will overwrite by the decorator function.

Functools will properly update the metadata on wrapped functions
"""

def decor(func):
    def wrap(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return return_value
    wrap.__name__=func.__name__
    wrap.__doc__=func.__doc__
    return wrap

@decor
def hello(name):
    "Print the name"
    print("Hello {}".format(name))

print(hello.__name__)
print(hello.__doc__)
print(help(hello))

import functools

def decor(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return return_value
    return wrap

@decor
def hello(name):
    "Print the name"
    print("Hello {}".format(name))

print(hello.__name__)
print(hello.__doc__)
print(help(hello))