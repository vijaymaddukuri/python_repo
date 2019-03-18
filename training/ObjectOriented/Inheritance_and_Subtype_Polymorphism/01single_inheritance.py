"""
Single Inheritance: Subclasses will want to initialize base class

Base class initializer will call automatically if subclass initializer is not defined

Other languages automatically call base class initializer

Python treats __init__ like any other function

Base class __init__() is not called if overridden.

Use super() to call base class __init__()
"""

class Base:
    def __init__(self):
        print('Base initializer')
        self.val = 'Vijay'

    def f(self):
         print('Base f()')

class SubClass(Base):
    def __init__(self):
        super().__init__()
        print(self.val)
        print('Subclass initializer')
    
    def f(self):
        print('Sub f()')

s = SubClass()
s.f()
