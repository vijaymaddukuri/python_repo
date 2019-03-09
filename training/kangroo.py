"""
You are choreographing a circus show with various animals.
For one act, you are given two kangaroos on a number line ready to jump in the positive direction
(i.e, toward positive infinity).

The first kangaroo starts at location x1 and moves at a rate of  v1 meters per jump.
The second kangaroo starts at location x2 and moves at a rate of  v2 meters per jump.

Complete the function kangaroo in the editor below.
It should return YES if they reach the same position at the same time, or NO if they don't.

kangaroo has the following parameter(s):

x1, v1: integers, starting position and jump distance for kangaroo 1
x2, v2: integers, starting position and jump distance for kangaroo 2
"""

def kangaroo(x1, v1, x2, v2):
    if (x2 > x1 and v2 >= v1):
        return "NO"

    if (x1 - x2) % (v2 - v1) == 0:
        return 'YES'
    else:
        return 'NO'

print(kangaroo(0, 3, 4, 2))
print(kangaroo(0, 2, 5, 3))