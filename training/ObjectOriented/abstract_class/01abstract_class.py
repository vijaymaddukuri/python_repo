"""
Abstract Classes in Python:

An abstract class can be considered as a blueprint for other classes,
allows you to create a set of methods that must be created within any child classes built from your abstract class.
A class which contains one or abstract methods is called an abstract class.
An abstract method is a method that has declaration but not has any implementation.
Abstract classes are not able to instantiated and it needs subclasses to provide implementations for those abstract methods
which are defined in abstract classes. While we are designing large functional units we use an abstract class.
When we want to provide a common implemented functionality for all implementations of a component, we use an abstract class.
Abstract classes allow partially to implement classes when it completely implements all methods in a class, then it is called interface.

"""

from abc import ABC, abstractmethod


class Polygon(ABC):

    # abstract method
    def noofsides(self):
        pass


class Triangle(Polygon):

    # overriding abstract method
    def noofsides(self):
        print("I have 3 sides")


class Pentagon(Polygon):

    # overriding abstract method
    def noofsides(self):
        print("I have 5 sides")


class Hexagon(Polygon):

    # overriding abstract method
    def noofsides(self):
        print("I have 6 sides")


class Quadrilateral(Polygon):

    # overriding abstract method
    def noofsides(self):
        print("I have 4 sides")

    # Driver code


R = Triangle()
R.noofsides()

K = Quadrilateral()
K.noofsides()

R = Pentagon()
R.noofsides()

K = Hexagon()
K.noofsides() 