def fun(x, lst=[]):
    for i in range(x):
        lst.append(i)
    print(lst)

fun(5)
fun(2, [100, 200])
fun(3)
fun(2, [101, 201])


i=10
print("i=",i, "id(i) =", id(i))
def fun():
    i = 20
    print("i=",i, "id(i) =", id(i))

fun()
print("i=",i, "id(i) =", id(i))

print('##################')

i=10
print("i=",i, "id(i) =", id(i))
def fun():
    """If we want change the global scope"""
    global i
    i = 20
    print("i=",i, "id(i) =", id(i))

fun()
print("i=",i, "id(i) =", id(i))