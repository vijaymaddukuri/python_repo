from itertools import islice, count

thousand_primes=islice((x for x in count()), 1000)
print(list(thousand_primes))

print(all(t>0 for t in [1,2,3,4,-1]))