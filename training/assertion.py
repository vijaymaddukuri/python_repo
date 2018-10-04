test=0
fail=0

try:
    test += 1
    assert 1 == 1, 'inequal'
except AssertionError:
    fail+=1
    
def power(x,n):
    return x ** n
try:
    test += 1
    assert power(4,3) == 65, 'test failed'

except AssertionError:
    fail+=1

print('{}/{}'.format(test, fail))