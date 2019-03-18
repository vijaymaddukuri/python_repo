"""
Maximum number of integers that can be removed from the two stacks without the sum of elements in A and B not
exceeding x.
"""

def twoStacks(x, a, b):
    a = a[::-1]
    b = b[::-1]
    n = len(a)
    m = len(b)
    total = 0
    itemList = []
    for i in range(n):
        val = a.pop()
        if total + val > x:
            break
        total += val
        itemList.append(val)

    max_count = len(itemList)
    cur_count = max_count
    while m:
        if total + b[-1] <= x:
            total += b.pop()
            m -= 1
            cur_count += 1
            if cur_count > max_count:
                max_count = cur_count
            continue
        if not len(itemList):
            break
        aval = itemList.pop()
        total -= aval
        cur_count -= 1
    return max_count

print(twoStacks(10, [4,2,4,6,1], [2,1,8,5]))