"""
Apply a function to each element in a sequence,
constructing a new sequence with the elements for which the function returns True

Unlike map(), filter accepts only single argument, it evaluates lazily like map.

We can give fist argument as none in filter
"""
trues=filter(None, [1, 0, True, False, "vijay"])
print(list(trues))

def is_odd(n):
    return n%2!=0
print(list(filter(is_odd, [1,2,3,4])))

positives = filter(lambda x: x>0, [1,2,-1,-3,4])
print(list(positives))
