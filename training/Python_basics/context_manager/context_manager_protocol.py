"""
Context Manager:

An object designed to be used in a with-statement
Which ensures that resources are properly and automatically managed

__enter__():
called before entering into the with-statement body
Return value bound to as variable
can return value of any type
commonly returns context-manager itself

__exit__():
Called when with-statment body exists
Can check type for None to see if an exception was thrown

"""

class LoggingcontextManager:
    def __enter__(self):
        print('LoggingcontextManager.__enter__()')
        return 'You are in a with-block!'
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print('LoggingcontextManager.__exit() exits normally')
        else:
            print('LoggingcontextManager.__exit({}, {}, {})'.format(exc_type,exc_val,exc_tb))
        return

# with LoggingcontextManager() as x:
#     print(x)

with LoggingcontextManager() as y:
    raise ValueError('Somthing went wrong')

