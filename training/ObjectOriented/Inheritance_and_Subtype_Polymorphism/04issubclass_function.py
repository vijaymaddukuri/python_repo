"""
issubclass(): Determines if one type is a subclass of another
"""

class MyInt(int): pass

class subInt(MyInt): pass

print(issubclass(subInt, MyInt))
print(issubclass(MyInt, subInt))
print(issubclass(subInt, int))