"""
classmethod() Parameters
The classmethod() method takes a single parameter:

function - Function that needs to be converted into a class method

Return value from classmethod()
The classmethod() method returns a class method for the given function.

What is a class method?
A class method is a method that is bound to a class rather than its object. It doesn't require creation of a class instance, much like staticmethod.

The difference between a static method and a class method is:

Static method knows nothing about the class and just deals with the parameters
Class method works with the class since its parameter is always the class itself.
"""

class Person:
    age = 25

    def printAge(cls):
        print('The age is:', cls.age)

# create printAge class method
Person.printAge = classmethod(Person.printAge)

Person.printAge()