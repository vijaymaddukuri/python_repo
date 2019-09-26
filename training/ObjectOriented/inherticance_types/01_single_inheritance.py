class Computer():
    def __init__(self, computer, ram, ssd):
        self.computer = computer
        self.ram = ram
        self.ssd = ssd

class Laptop(Computer):
    def __init__(self, computer, ram, ssd, model):
        super().__init__(computer, ram, ssd)
        self.model = model

lenovo = Laptop('lenovo', 2, 512, 'l420')
print('This laptop is:', lenovo.computer)
print('This laptop has ram of', lenovo.ram)
print('This laptop has ssd of', lenovo.ssd)
print('This laptop has this model:', lenovo.model)


"""
In the above example, we have defined one base class which is Computer, and one is derived class which is Laptop.

We have defined three properties inside the base class, and the derived class has total four properties. 

Three properties from derived class are derived from the base class, and fourth is that’s own property. 
In the derived or child class has its model property. Other three are obtained from base class Computer.

So, now if we only create an object of the derived class, we still have all the access of the base class’s property 
because of super() function.
"""