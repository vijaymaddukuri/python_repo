Big O Notation:
	Big-O notation describes how quickly runtime will grow relative to the input as the input get arbitrarily large.

Python Method vs Function

 - Method is called by its name, but associated to an object ( dependent).
 - It may or may not return any data
 - A method can operate on the data (instance variables) that is contained by the corresponding class
		# User-Defined  Method
		class ABC :
			def method_abc (self):
				print("I am in method_abc of ABC class. ")

		class_ref = ABC() # object of ABC class
		class_ref.method_abc()

		# Inbuilt method :

		import math

		ceil_val = math.ceil(15.25)
		print( "Ceiling value of 15.25 is : ", ceil_val)

  - Function is block of code that is also called by its name. (independent)
  - The function can have different parameters or may not have any at all. If any parameters are passed,
  they are passed explicitly.
  - Function does not deal with Class and its instance concept.
		# User-Defined Function :

		def Subtract (a, b):
			return (a-b)

		# Inbuilt Function :

		s = sum([5, 15, 2])
		print( s ) # prints 22


 - Difference between method and function

	Simply, function and method both look similar as they perform in almost similar way, but the key difference
	is the concept of ‘Class and its Object‘.

	Functions can be called only by its name, as it is defined independently. But methods can’t be called by
	its name only, we need to invoke the class by a reference of that class in which it is defined,
	i.e. method is defined within a class and hence they are dependent on that class.

Python Module: Convenient import with API
Python Script: Convenient execution from cmd line
Python Program: Composed of many modules

PASS By Object Reference:

The value of the reference is copied not the value of object

Python is Dynamic and strong:

Dynamice type system:

    In Dynamic type system object types are only resolved at run time.

Strong type System:

    No implicit type conversion

Python Name scopes:

    Scopes are contexts in which named references can be looked up

Types:

- Local (Inside the current function)
- Enclosing (Any and all enclosing functions)
- Global (Top-level of module)
- Build-in Provided by the builtins module

Exceptions:

Programmer errors:

IndentationError
SyntaxError
NameError

Comprehensions: Short-hand syntax for creating collections and iterable objects

Concise syntax for describing lists, sets and dicts
Types of comprehensions:

 - List comprehensions.
 - set comprehensions
 - Dict comprehensions

List comprehensions:

[i for i in range(20)]

Set comprehensions:

{i for i in range(20)}

Dict comprehensions:

country_to_cap = {'India': 'Delhi'}
cap_country = {cap: country for country, cap in country_to_cap.items()}

Iteration Protocols:

Iterable protocol:

Iterable objects can be passed to the built-in iter() function to get an iterator

iterator= iter(iterable)

Iterator protocol:

Iterator objects can be passed to the built-in next() function to fetch the next item.

Generator in python:

- Specify iterable sequences
  - All generators are iterators

- Are lazily evaluated
 - the next value in the sequence is computed on demand

- Can model infinite sequences
  - Such as data streams with no definite end

- Are composable into pipeline
  - For natural stream processing

Stateful generators:
 - Generators resume execution
 - Can maintain state in local variables
 - complex control flow
 - Lazy evaluation

Generators are single used objects, each time we call a generator, the function it creates a new generator object

Generator function allows us to describe series using imperative code
Gen function contain atleast one yield keyword
Gen are iterators. When advanced with next() the generator stars and resumes execution up and including next yield
Each call to generator function creates new gen object
Generators can maintain explicit state in local variables between iter.
Gens are lazy and so can model infinite series of data


Iteration tools:

sum()
any()
zip()
all()
min()
max()
enumerate()

Standard lib itertool modules:

chain()
islice()
count()

CLASSES:

When python built-ins are not right for the job, we can use classes to create custom type

Classes define the structure and behavior of an object
An object's class define its initialization

Method: Functions defined inside a class
Instance Method: Functions which can be called on objects
self: The first argument to all instance methods
__init__(): Instance method for initializing new objects, it is an initializer not the constructor.

_number:
1. Avoid name clash with number()
2. By convention, implementation details start with _

Djngo project:
 python manage.py startapp saltmanager

Polymorphism:

Using objects of different types through common interface

--------------------------------------------------------------------

Absolute path for importing:

	from onb.common import function

Relative importing:

	can reduce typing in deeply nested package structure.

	Promotes certain forms of modifiablity

	can aid package renaming and refactoring

		from .commom import function

		from . import function

--------------------------------------------------------------------
Dunder all (__all__):

List of attribute names imported via from module import *.

Generally when import * used all modules will import locally. To limit few imports use __all__

The __all__ attribute should be list of strings containing names available in the module.

__init__.py
	__all__ = ['mod1', 'mod2']

__all__ is a useful tool for limiting what names we exposed for our modules.

----------------------------------------------------------------------

Executable directories:

Directories containing any entry points for python execution

Namespace Packages:

Packages split across several directories. Useful for splitting large packages into multiple parts.

Avoids complex initialization ordering problems.

Importing namespace packages:

 - Python scans all entries in sys.path
 - If matching dir with __init__.py is found, a normal package loaded.
 - If foo.py found, then it is loaded
 - Otherwise, all matching dir in sys.path are considered part of the namespace package.


Callable classes:

Calling a class will invokes the constructor.

Class attributes vs Instance attributes:


----------------------------------------------------------------------------


Stacks Queues and Deques:

Stacks:

A stack is an ordered collection of items where the addition of new items and the removal of existing items always take place in
the same end.

This end commonly referred as the top.

The opposite end of the top is base.

The base of the stack is siginificant since items stored in the stack, that are closer to the base represent those that have been in the stack the longest


Most recently added item is the one that is in position to be removed first. (LIFO)

Newers items are near to the top, older items near to the base.

Order of insertion is the reverse of order of removal.

Example: Every web browser has a back button.

As you navigate from web page to web page, those pages are placed on a stack (URLS that are going on the stack).

***********************************************************

Queue:

A queue is an ordered collection of items where the addition of new items happens at one end, called the rear.

And the removal of existing items occurs at the other end, commonly called the front.

As an element enters into the queue, it starts at the rear and makes its way toward the front, waiting until that time
when it is the next element to be removed.

Most recently added item in the queue must wait at the end of the collection (FIFO) or (FCFS)

Example: Movie ticket queue or grocery store queue.

Enqueue: Adding item to queue
Dequeue: Removing front item from the queue

***********************************************************

Deque:

A deque also known as double ended queue, is an ordered collection of items similar to the queue.

It has two ends front and rear and the items remain positioned in the collection.

Unrestricted nature of adding and removing items makes deque different.

New items can be added at either the front or the rear.

Likewise, existing items can be removed from either end.

This hybrid linear structure provides all the capabilities of stacks and queues in a single data structure.



---------------------------------------------------------------------------------------

BlockChain:

A distributed data storage consisting of containers(blocks) on different machines which are connected.

A block chain is a data store, a single block can hold any data.

Ex: List of transactions in bit coin.

We have multiple blocks in blockchain, which knows about each other.

We can manuplate data in block chain, because it is distributed among multiple machines.

Each block is hashed, other blocks will save the hash of previous block.

When input changes in the one block, other block recoginzes the changes (which is very important for security)

What is crypto currency:

Distributed secured data storage.

If the data you store in a block is a list of transactions, the coins transferred in the transactions form your cryto currency, which are distributed in many systems.

Coins are transferred with transactions, changing them into other currency is not possible inside the block chain

Coins are created via mining(as a reward for the effort)

----------------------

Object Base: Using existing pre-defined objects

object oriented: Any real world objects on the fly.

Polymorphism is based on the greek words Poly (many) and morphism (forms).
We will create a structure that can take or use many forms of objects.

Sometimes an object comes in many types or forms. If we have a button,
there are many different draw outputs (round button, check button, square button,
button with image) but they do share the same logic: onClick().  We access them using the same method .
This idea is called Polymorphism.


Abstraction: It is a interface, which provides only required information, by hiding other data like implementation.
Encapsulation: Blueprint where we create entity (type and behaviours). Hiding data.
Polymorphism
Message parsing
Inheritnace


Shallow copy: A reference of object is copied in other object. It means any change made to a copy of object do reflect
in the original object

Shallow copy: i=10 and j=10 will have the same id, because value is same,
 within the same scope. The id will exist if it have same references.

Deep copy: A copy of object is copied into another object. It means changes made to a copy of object
do not reflect in the original object

Creates a copy of the object and the elements of the object.

Remove id from garbage - del(i)

Duck typing
There is another concept in this typing lark that is a feature of dynamic languages.
This is duck typing. The idea is that it doesn't actually matter what type my data is -
just whether or not I can do what I want with it.

For example in a statically typed language we have a concept of adding.
Some types of object can be added - usually only to objects of the same type.
(Although most languages will let you add an integer to a floating point number - resulting in a floating point number). Try to add different types of objects together and the compiler will tell you that you're not allowed to


Function:

In 2.x  Object and type are different
In 3.x: All considers as one object

If we want to get base class intitilazer(__init__) varialbes, we need to use super() in derived class.

super(Base, self).__init__(self)

map():

Apply a function to every element in a sequence, produce a new sequence.

It performs lazy evaluation, it only produces values as they are needed.

map() can accept any number of input sequence

The number of input sequences must match the number of function arguments.

filter():

Apply a function to each element in a sequence, constructing a new sequence with the elements
for which the function returns True

Unlike map(), filter accepts only single argument, it evaluates lazily like map.

We can give fist argument as none in filter

In Python2, map() and filter() are eagerly evaluated and return list object.

reduce():

Repeatedly apply function to the elements of a sequence, reducing them to a single value

Optional initial value is conceptually just added to the start of the input sequence.

iterable: An object which implements the __iter__() method

iterator: An object which implements the iterable protocol.


Single Inheritance: Subclasses will want to initialize base class

Base class initializer will call automatically if subclass initializer is not defined

Other languages automatically call base class initializer

Python treats __init__ like any other function

Base class __init__() is not called if overridden.

Use super() to call base class __init__()


items = [1, 2, 3, 4, 5]
def sqr(x): return x**2

square1 =list(map(sqr,items))
square2 = list(map((lambda x: x **2), items))
power=list(map(pow,[2, 3, 4], [2, 2, 2]))
print(power)
fil=list( filter((lambda x: x < 0), range(-5,5)))
# reduceItem=reduce( (lambda x, y: x * y), [1, 2, 3, 4] )
# print(reduceItem)
a=[[1,2,3,4],[4,5,6,7]]
b=[4,5,6,7]
print(list(zip(*a)))
print(list(zip(a,b)))

print(all(['a','','c'])) #Return True if all elements of the iterable are true (or if the iterable is empty).
print(any(['a','','c'])) #Return True if any element of the iterable is true. If the iterable is empty, return False.
print(bin(128)[2:].zfill(8)) #Decimal to binary
print("{0:08b}".format(128))
arr = ("{0:b}".format(5))
print(int('10000000',2)) #Binary to decimal
print(chr(97))  #Return a string of one character whose ASCII code is the integer
print(ord('a')) #Return a ASCII code of a string
#print(cmp(x, y) #The return value is -1 if x < y, zero if x == y and strictly 1 if x > y.
print(dir([object])) #Without arguments, return the list of names in the current local scope. With an argument, attempt to return a list of valid attributes for that object.
print(divmod(1,2)) #(a // b, a % b)
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
print(list(enumerate(seasons, start=1))) #output: [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
print(eval('1+1')) #returns 2
print(hex(255)) #'0xff'
print(min([1,2,3]))
print(max([1,2,3]))
# prints the official format of date-time object
print(repr(1))
# Prints readable format for date-time object
print(str(1))
s='a'
print('---------------------')
# print(s.extend('1'))
s=[1,2,3,4]


'''
Generators:

Generators are iterators,but you can only iterate over them once.

It's because they do not store all the values in memory,they generate the values on the fly:

Generators simplifies creation of iterators.

A generator is a function that produces a sequence of results instead of a single value.

When a generator function is called, it returns a generator object without even beginning execution of the function.

When next method is called for the first time,the function starts executing until it reaches yield statement.

The yielded value is returned by the next call.

Yield:

Yield is a keyword that is used like return, except the function will return a generator.

Range and Xrange:

Using xrange is safe when dealing with larger numbers,.
The range python function create a list with elements equal to number
we given to that range where as xrange create one element at any given time.
This saves use to reduce the usage of RAM.

'''

'''
with

when you have two related operations which you’d like to execute as a pair, with a block of code in between.

Object:

A unique instance of a data structure that's defined by its class.
An object comprises both data members (class variables and instance variables) and methods.

Object is simply a collection of data (variables) and methods (functions) that act on those data.
And, class is a blueprint(for the object.

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

A namespace containing all the built-in names is created when we start the Python interpreter and
exists as long we don't exit.

This is the reason that built-in functions like id(), print() etc. are always available to us
from any part of the program. Each module creates its own global namespace.

These different namespaces are isolated. Hence, the same name that may exist in different modules do not collide.
'''

List vs Tuple:

List:

The important characteristics of Python lists are as follows:

    Lists are ordered.
    Lists can contain any arbitrary objects.
    List elements can be accessed by index.
    Lists can be nested to arbitrary depth.
    Lists are mutable.
    Lists are dynamic.

If s is a string, s[:] returns a reference to the same object

Conversely, if a is a list, a[:] returns a new object that is a copy of a

Tuple:

Tuples are an ordered sequences of items, just like lists.
The main difference between tuples and lists is that tuples cannot be changed (immutable)
unlike lists which can (mutable).

It is important to keep in mind that if you want to create a tuple containing only one value, you need a trailing comma after your item.

# tuple with one value
tup1 = ('Vijay',)

Even though tuples are immutable, it is possible to take portions of existing tuples to create new tuples as the following example demonstrates.

# Initialize tuple
tup1 = ('Python', 'SQL')
# Initialize another Tuple
tup2 = ('R',)
# Create new tuple based on existing tuples
new_tuple = tup1 + tup2;
print(new_tuple)

Lists and tuples are standard Python data types that store values in a sequence.
A tuple is immutable whereas a list is mutable.

Tuples are faster than lists. If you're defining a constant set of values and all you're ever going
to do with it is iterate through it, use a tuple instead of a list.

It makes your code safer if you “write-protect” data that does not need to be changed.
Using a tuple instead of a list is like having an implied assert statement that this data is constant,
and that special thought (and a specific function) is required to override that.

Some tuples can be used as dictionary keys (specifically, tuples that contain immutable values like strings,
numbers, and other tuples). Lists can never be used as dictionary keys, because lists are not immutable.

Tuples can be used as values in sets whereas lists can not


Example:

a = ["apples", "bananas", "oranges"]

When you do this, a python object of type list is created in the memory and the variable

Now if you modify the first index of the list, and check the id() again, you will get the same exact value because
a is still referring to the same object.

Now, let’s see what happens if we perform the same thing on tuples.

>>> a = ("apples", "bananas", "oranges")
>>> id(a)
4340765824
>>> a = ("berries", "bananas", "oranges")
>>> id(a)
4340765464

This means that after the second assignment, a is referring to an entirely new object.

Moreover, if no other variables in your program is referring to the older tuple then python’s garbage collector
will delete the older tuple from the memory completely.

So there you have it, this concept of mutability is the key difference between lists and tuples.

Mutability is more efficient when you know you will be frequently modifying an object.

For example, assume you have some iterable object (say x), and you want to append each element of x to a list.

L  = []
for item in x:
    L.append(item)

But can you even imagine what would happen if we had used a tuple instead?

T  = ()
for item in x:
    T = T + (item,)

Since tuples are immutable, you are basically copying the contents of the tuple T to a new tuple object
at EACH iteration.



Easiness of debugging: Immutability Wins!:

Let’s take a look at this very simple example.

>>> a = [1, 3, 5, 7]
>>> b = a
>>> b[0] = -10
>>> a
[-10, 3, 5, 7]

Notice that when we do b = a, we are not copying the list object from b to a.

We are actually telling python that the two variables a and b should reference the same list object.

Because a effectively holds the location of the python object in memory, when you say b = a you copy that address location (not the actual object) to b.

This results in having two references (a and b) to the same list object.

In other words when we do b[0] = -10, it has the same effect as a[0] = -10.

Of course you can look at the code and rightfully think that it is easy to debug.

Well you are right for small snippets of code like this, but imagine if you have a big project with many references to the same mutable object.

It will be very challenging to track all the changes to this object because any modification by any of those references will modify the object.

This is not the case with immutable objects even if you have multiple references to them.

Once an immutable object is created, its content will never change.

Easiness of debugging: Immutability Wins!


Memory Efficiency:

Memory efficiency: Immutability Wins

if you create immutable objects that hold the same value, python (under certain conditions) might bundle
these different objects into one.

>>> a = "Karim"
>>> b = "Karim"
>>> id(a)
4364823608
>>> id(b)
4364823608

As you can see, even though in our python program we explicitly created two different string objects,
python internally bundled them into one.

Python was able to do that because the immutability of strings makes it safe to perform this bundling.

Not only that this will save us some memory (by not storing the string multiple times in memory),
but also every time you want to create a new object with the same value,
python will just create a reference to the object that already exists in memory which is definitely more efficient.

Ref: https://www.afternerd.com/blog/difference-between-list-tuple/






