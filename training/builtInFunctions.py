items = [1, 2, 3, 4, 5]
def sqr(x): return x**2

square=list(map(sqr,items))
square = list(map((lambda x: x **2), items))
power=list(map(pow,[2, 3, 4], [10, 11, 12]))
fil=list( filter((lambda x: x < 0), range(-5,5)))
reduceItem=reduce( (lambda x, y: x * y), [1, 2, 3, 4] )
print reduceItem
a=[[1,2,3,4],[4,5,6,7]]
b=[4,5,6,7]
print zip(*a)
print zip(a,b)

print all(['a','','c']) #Return True if all elements of the iterable are true (or if the iterable is empty).
print any(['a','','c']) #Return True if any element of the iterable is true. If the iterable is empty, return False.
print bin(128)[2:].zfill(8) #Decimal to binary
print "{0:08b}".format(128)
print int('10000000',2) #Binary to decimal
print chr(97)  #Return a string of one character whose ASCII code is the integer
print ord('a') #Return a ASCII code of a string
#print cmp(x, y) #The return value is -1 if x < y, zero if x == y and strictly 1 if x > y.
print dir([object]) #Without arguments, return the list of names in the current local scope. With an argument, attempt to return a list of valid attributes for that object.
print divmod(1,2) #(a // b, a % b)
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
print list(enumerate(seasons, start=1)) #output: [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
print eval('1+1') #returns 2
print hex(255) #'0xff'
print min([1,2,3])
print max([1,2,3])
# prints the official format of date-time object
print repr(1)
# Prints readable format for date-time object
print str(1)
s='a'
print '---------------------'
print s.extend('1')
s=[1,2,3,4]


'''
Generators:

Generators are iterators,but you can only iterate over them once.

It's because they do not store all the values in memory,they generate the values on the fly:

Generators simplifies creation of iterators. A generator is a function that produces a sequence of results instead of a single value.

When a generator function is called, it returns a generator object without even beginning execution of the function.

When next method is called for the first time,the function starts executing until it reaches yield statement.

The yielded value is returned by the next call.

Yield:

Yield is a keyword that is used like return, except the function will return a generator.

Range and Xrange:

Using xrange is safe when dealing with larger numbers,.
The range python function create a list with elements equal to number we given to that range where as xrange create one element at any given time.
This saves use to reduce the usage of RAM.

'''

'''
with

when you have two related operations which you’d like to execute as a pair, with a block of code in between.

Object:

A unique instance of a data structure that's defined by its class.
An object comprises both data members (class variables and instance variables) and methods.

Object is simply a collection of data (variables) and methods (functions) that act on those data. And, class is a blueprint for the object.

A class creates a new local namespace where all its attributes are defined. Attributes may be data or functions.

As soon as we define a class, a new class object is created with the same name.

This class object allows us to access the different attributes as well as to instantiate new objects of that class.

Instantiation:
we can create many objects from a class.

An object is also called an instance of a class and the process of creating this object is called instantiation.


NameSpace:

To simply put it, namespace is a collection of names.

In Python, you can imagine a namespace as a mapping of every name, you have defined, to corresponding objects.

Different namespaces can co-exist at a given time but are completely isolated.

A namespace containing all the built-in names is created when we start the Python interpreter and exists as long we don't exit.

This is the reason that built-in functions like id(), print() etc. are always available to us from any part of the program. Each module creates its own global namespace.

These different namespaces are isolated. Hence, the same name that may exist in different modules do not collide.
'''