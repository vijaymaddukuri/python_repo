"""
If class has multiple base classes and second base class defines no initializer, then only the initializer of the
first base class will be called.
"""

class Base1:
    def __init__(self):
        print('Base1 call')

class Base2:
    def __int__(self):
        print('Base2 call')

class SubClass(Base1, Base2):
    pass

s = SubClass()

"""
__bases__: A tuple of base class
"""
print(SubClass.__bases__)
