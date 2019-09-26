"""
In an object oriented python program,
you can restrict access to methods and variables.
This can prevent the data from being modified by accident and is known as encapsulation.
"""

"""
Private method

Restricted accesss to methods or variable

We create a class Car which has two methods:  drive() and updateSoftware().  
When a car object is created, it will call the private methods __updateSoftware(). 

This function cannot be called on the object directly, only from within the class.
"""

class Car:

    def __init__(self):
        self.__updateSoftware()

    def drive(self):
        print('driving')

    def __updateSoftware(self):
        print('updating software')

redcar = Car()
redcar.drive()
# redcar.__updateSoftware()  #not accesible from object.

"""
Private variables:

Class with private variables
Variables can be private which can be useful on many occasions. 
A private variable can only be changed within a class method and not outside of the class.

"""

class Car:

    __maxspeed = 0
    __name = ""

    def __init__(self):
        self.__maxspeed = 200
        self.__name = "Supercar"

    def drive(self):
        print('driving. maxspeed ' + str(self.__maxspeed))

    def setMaxSpeed(self,speed):
        """
        If you want to change the value of a private variable, a setter method is used.
        This is simply a method that sets the value of a private variable.
        :param speed:  Speed val
        :return:  updated speed value
        """
        self.__maxspeed = speed

redcar = Car()
redcar.drive()
redcar.__maxspeed = 10  # will not change variable because its private
redcar.drive()
redcar.setMaxSpeed(320)
redcar.drive()