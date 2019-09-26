"""
The biggest reason for using a @classmethod is in an alternate constructor that is intended to be inherited.
This can be very useful in polymorphism. An example:
"""

class Shape(object):
    # this is an abstract class that is primarily used for inheritance defaults
    # here is where you would define classmethods that can be overridden by inherited classes
    @classmethod
    def from_square(cls, square):
        # return a default instance of cls
        return cls()

class Square(Shape):
    def __init__(self, side=10):
        self.side = side

    @classmethod
    def from_square(cls, square):
        return cls(side=square.side)


class Rectangle(Shape):
    def __init__(self, length=10, width=10):
        self.length = length
        self.width = width

    @classmethod
    def from_square(cls, square):
        return cls(length=square.side, width=square.side)


square = Square(3)

for polymorphic_class in (Square, Rectangle):
    this_shape = polymorphic_class.from_square(square)
    print(this_shape)