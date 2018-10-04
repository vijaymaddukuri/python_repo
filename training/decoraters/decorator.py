"""
Replace enhance or modify exisiting functions
DOes not change the original function defination
Calling code doesnot need to change
Decorator mechanism uses the modified functions original name

Validating functional arguments is one valid use case
"""

def argument_logger(func):
    """Decorator"""
    def logger_handler(*args, **kwargs):
        """Decorator Handler"""
        return_value=func(*args)
        print("args: {} returns: {}".format(args, return_value))
        return return_value
    return logger_handler

@argument_logger
def power(x,n):
    return x ** n

def escape_unicode(func):
    def wrap(*args, **kwargs):
        return_Value = func(*args, **kwargs)
        print('returns: {}'.format(return_Value))
        return ascii(return_Value)
    return wrap

@escape_unicode
def northern_city():
    return 'Troms&'

print(power(4,5))
print(northern_city())