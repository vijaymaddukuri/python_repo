"""
You have three stacks of cylinders where each cylinder has the same diameter,
but they may vary in height. You can change the height of a stack by removing and discarding its topmost cylinder
any number of times.

Find the maximum possible height of the stacks such that all of the stacks are exactly the same height.
This means you must remove zero or more cylinders from the top of zero or more of the three stacks until
they're all the same height, then print the height.

The removals must be performed in such a way as to maximize the height.
"""


def get_max_height(h1, h2, h3):
    sum_h1, sum_h2, sum_h3 = sum(h1), sum(h2), sum(h3)
    min_h = min(sum_h1, sum_h2, sum_h3)

    if min_h == 0:
        return 0

    matched = False
    while not matched:
        if sum_h1 > min_h:
            sum_h1 -= h1.pop(0)
        if sum_h2 > min_h:
            sum_h2 -= h2.pop(0)
        if sum_h3 > min_h:
            sum_h3 -= h3.pop(0)
        min_h = min(sum_h1, sum_h2, sum_h3)
        matched = (sum_h1 == sum_h2 == sum_h3)

    return min_h

print(get_max_height([3,2,1,1,1],[4,3,2],[1,1,4,1]))