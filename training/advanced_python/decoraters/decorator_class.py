class CallCount:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count+=1
        return_value=self.func(*args, **kwargs)

@CallCount
def hello(name):
    print('hello {}'.format(name))

hello('vijay')
hello('vj')
print(hello.count)

class Trace:
    def __init__(self):
        self.enable=True
    def __call__(self, func):
        def wrap(*args, **kwargs):
            if self.enable:
                print('calling {}'.format(func))
            return func(*args, **kwargs)
        return wrap

tracer = Trace()

@tracer
def rotate_list(l):
    return l[1:]+ [l[0]]

l = rotate_list([1,2,3])
print(l)

tracer.enable=False
l = rotate_list([1,2,3])
print(l)
