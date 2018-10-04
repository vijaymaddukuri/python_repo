def distinct(iterable):
    seen = set()
    for item in iterable:
        if item in seen:
            continue
        yield item
        seen.add(item)
def run_distinct():
    items=[5, 7, 7, 5, 6]
    for item in distinct(items):
        print(item)
run_distinct()
# millon_sqrs = (x*x for x in range(1, 1000))
# print(list(millon_sqrs))
#
# sum(x*x for x in range(1,100001))
