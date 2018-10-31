"""
Repeatedly apply function to the elements of a sequence, reducing them to a single value
"""

from functools import reduce
import operator

print(reduce(operator.add, [1,2,3]))

def mul(x,y):
    print('mul of x - {}  y - {}'.format(x,y))
    return x*y

print(reduce(mul, range(1,10)))

# Optional initial value is conceptually just added to the start of the input sequence.
values = []
print(reduce(operator.add, values, 0))

values = []
print(reduce(operator.mul, values, 1))