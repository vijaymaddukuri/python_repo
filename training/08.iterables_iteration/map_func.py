"""
map():

Apply a function to every element in a sequnece, produce a new sequnece.

It performs lazy evaluation, it only produces values as they are needed.

map() can accept any number of input sequneces

The number of input sequences must match the number of function arguments.


"""
class Trace:
    def __init__(self):
        self.enable = True
    def __call__(self, func):
        def log_fun(*args, **kwargs):
            if self.enable:
                print('calling {}'.format(func))
            return func(*args, **kwargs)
        return log_fun

result = map(Trace()(ord), 'The quick lazy brown fox')

print(next(result))

print(list(result))

def mul(x,y):
    return x*y

a=[2,3,4]
b=[2,3,9]

print(list(map(mul,a,b)))

def sqrt(x):
    return x*x
print([x for x in map(sqrt, range(5))])

