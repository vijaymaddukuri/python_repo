def is_prime (x): return True if x in [2,3] else not any (x % n == 0 for n in range (2, int (x ** 0.5) + 1))

def get_non_primes():
    number=1
    if number == 1:
        yield 1
    while True:
        if not is_prime(number):
            yield number
        number += 1


a = (get_non_primes())

for i in range(5):
    print(next(a))