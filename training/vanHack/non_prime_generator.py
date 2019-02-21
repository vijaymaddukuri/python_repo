"""
Given an integer k, print the first k non-prime positive integers, each on new line. For example if k = 5, the output would be:

1
4
6
8
9

Function Description:

Complete the function manipulate_generator, the function must manipulate the generator function.
so that the first k non-prime positive integers are printed, each on a separate line.

manipulate_genrator has following params

g: a generator
n: an integer
"""

def is_prime(num):
    if num<2:
        return False
    i = 2
    while i< (num+1)/2:
        if num%i == 0:
            return False
        i += 1
    return True

def get_non_primes():
    number=1
    while True:
        if number!=1:
            if not is_prime(number):
                yield number
        number += 1

a = (get_non_primes())

def manipulate_generator(generator, n):
    generator.send(next(a)-1)


def positive_integers_generator():
    n = 1
    while True:
        x = yield n
        if x is not None:
            n = x
        else:
            n += 1

k = 10
g = positive_integers_generator()
for _ in range(k):
    n = next(g)
    print(n)
    manipulate_generator(g, n)