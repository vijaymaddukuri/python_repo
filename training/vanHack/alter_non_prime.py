def is_prime(x): return True if x in [2,3] else not any (x % n == 0 for n in range (2, int (x ** 0.5) + 1))
count = 0
def manipulate_generator(generator, n):
    global count
    global k
    count += 1
    if count == k:
        return
    while True:
        if is_prime(n+1):
          n = next(generator)
        else:
            return

def positive_integers_generator():
    n = 1
    while True:
        x = yield n
        if x is not None:
            n = x
        else:
            n += 1
k = int(input())
g = positive_integers_generator()
for _ in range(k):
    n = next(g)
    print(n)
    manipulate_generator(g, n)