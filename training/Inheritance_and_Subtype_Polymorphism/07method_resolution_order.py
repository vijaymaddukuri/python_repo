"""
MRO: Ordering that determines method name lookup.

MRO is an ordering of the inheritance graph
"""

class Base1:
    def __init__(self):
        print('Base1 call')

    def func(self):
        print('Base1 func')

class Base2(Base1):
    def __int__(self):
        print('Base2 call')
    def func(self):
        print('Base2 func')

class SubClass(Base2, Base1):
    pass

s = SubClass()
s.func()

print(SubClass.__mro__)