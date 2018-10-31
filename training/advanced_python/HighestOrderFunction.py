def outer(oParam):
    def inner(iParam):
        print("oParam =", oParam, ", iParam = ", iParam)
        print("====")
    return inner

fn = outer(10)
print(fn)
fn(5)
fn(25)


def read():
    print("reading")

def write():
    print("writing job")
'''
print("Allocating resources")
read()
print("Releasing resources")
print("=======")

print("Allocating resources")
write()
print("Releasing resources")
print("=======")
'''

def callback(filesystem, fn):
    print("Allocating resources for filesystem", filesystem)
    fn()
    print("Releasing resources")
    print("=======")

callback('win32', read)
callback('ext2', write)



def callback(filesystem):
    print("Allocating resources for filesystem", filesystem)
    def wrapper(fn):
        fn()
    print("Releasing resources")
    print("=======")
    return wrapper

# callback('win32')
exFsys = callback('ext2')
exFsys(read)


print("logging started")
read()
print("logging ended")
print("==================")

print("logging started")
write()
print("logging ended")
print("==================")


def logging(func):

    def wrap(*args):
        print("started")
        return_value = func(*args)
        print("ended")
        return return_value
    return wrap


def add(x,y):
    return x + y

def sub(x,y):
    return x - y
sum = logging(add)
print(sum(1,2))

add = logging(add)
print(add(1,2))

print(add(1,2))
@logging
def add(x,y):
    return x + y
@logging
def sub(x,y):
    return x - y

print(add(1,2))