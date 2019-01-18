"""
Exceptions are arranged in an inheritance hierarchy
"""

print(IndexError.mro())
print(KeyError.mro())

def lookups():
    s = [1, 4, 5, 6]
    try:
        item = s[5]
    except LookupError:
        print("Handled IndexError")
    d = dict(a=65, b=66, c=45)
    try:
        value = d['x']
    except LookupError:
        print("Handled KeyError")

if __name__  ==  '__main__':
    lookups()