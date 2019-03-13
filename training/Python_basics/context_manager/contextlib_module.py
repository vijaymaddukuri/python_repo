"""
Contextlib: Standard library module for working with context managers

Provides utilities for common tasks involving the with statement

contextlib.contextmanager:

A decorator you can use to create new context managers

Lets you to define context-managers with simple control flow

It allows you to leverage the statefulness of generators

Need to use standard exception handling to propagate exceptions

Explicitly re-raise or dont catch to propagate exceptions

Swallon exceptions by not re-raising  them
"""
import sys
import contextlib

@contextlib.contextmanager
def logging_context_manager():
    print('LoggingcontextManager.__enter__()')
    try:
        yield 'You are in a with-block!'
        print('LoggingcontextManager.__exit() exits normally')
    except:
        print('LoggingcontextManager.__exit()', sys.exc_info())
        raise

with logging_context_manager() as x:
    print(x)

print('\n******************\n')
with logging_context_manager() as y:
    raise ValueError('Somthing went wrong')


