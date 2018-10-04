def first(iterable):
    iterator = iter(iterable)
    try:
        return next(iterator)
    except  StopIteration:
        raise ValueError("Iterable is empty")

first([1,2,3])
first({1,2,3})
# first(set())

