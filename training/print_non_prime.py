def is_prime (x): return True if x in [2,3] else not any (x % n == 0 for n in range (2, int (x ** 0.5) + 1))
def is_prime2 (x):
    if x in [2, 3]:
        return True
    else:
        l = []
        for n in range(2, int(x ** 0.5) + 1):
            if x % n == 0:
                return False
        else:
            return True
def non_prime(num):
    non_prime = [1]
    x = 2
    while num:
        if not is_prime(x):
            non_prime.append(x)
            if len(non_prime) == num:
                num = 0
        x+=1
    return non_prime

print(non_prime(10))

