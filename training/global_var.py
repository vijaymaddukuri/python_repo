"""
Global variables are the one that are defined and declared outside a function
and we need to use them inside a function.
"""


# This function uses global variable s
def f():
    print(s)


# Global scope
s = "I love Geeksforgeeks"
f()

"""
If a variable with same name is defined inside the scope of function as well
then it will print the value given inside the function only and not the global value.
"""


# This function has a variable with
# name same as s.
def f():
    s = "Me too."
    print(s)


# Global scope
s = "I love Geeksforgeeks"
f()
print(s)

"""
The variable s is defined as the string “I love Geeksforgeeks”, before we call the function f().
The only statement in f() is the “print s” statement.
As there is no local s, the value from the global s will be used.

The question is, what will happen,
if we change the value of s inside of the function f()?
Will it affect the global s as well? We test it in the following piece of code:
"""


# def f():
#     print(s)
#
#     # This program will NOT show error
#     # if we comment below line.
#     s = "Me too."
#
#     print(s)
#
#
# # Global scope
# s = "I love Geeksforgeeks"
# f()
# print(s)

"""
To make the above program work, we need to use “global” keyword.
We only need to use global keyword in a function if we want to do assignments / change them.
global is not needed for printing and accessing.
Why? Python “assumes” that we want a local variable due to the assignment to s inside of f(),
so the first print statement throws this error message.
Any variable which is changed or created inside of a function is local,
if it hasn’t been declared as a global variable.
To tell Python, that we want to use the global variable,
we have to use the keyword “global”, as can be seen in the following example:
"""


# This function modifies global variable 's'
def f():
    global s
    print(s)
    s = "Look for Geeksforgeeks Python Section"
    print(s)


# Global Scope
s = "Python is great!"
f()
print(s)


a = 1

# Uses global because there is no local 'a'
def f():
    print('Inside f() : ', a )

# Variable 'a' is redefined as a local
def g():
    a = 2
    print('Inside g() : ',a)

# Uses global keyword to modify global 'a'
def h():
    global a
    a = 3
    print('Inside h() : ',a)

# Global scope
print('global : ',a)
f()
print('global : ',a)
g()
print('global : ',a)
h()
print('global : ',a)
