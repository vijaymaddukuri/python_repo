"""
Exceptions propagated by inner context managers can be seen by outer context managers
"""
import contextlib

@contextlib.contextmanager
def next_test(name):
    print('Entering', name)
    yield name
    print('Exiting', name)

with next_test('outer') as o, next_test('inner, nested in ' + o) as i:
    print('Body')

print('\n**********\n')
@contextlib.contextmanager
def propagrater(name, propagate):
    try:
        yield
        print('Normal exit')
    except:
        print(name, 'Received an exception')
        if propagate:
            raise

with propagrater('outer', True), propagrater('inner', False):
    raise TypeError('Cannot convert lead into gold')
print('\n**********\n')
with propagrater('outer', False), propagrater('inner', True):
    raise TypeError('Cannot convert lead into gold')