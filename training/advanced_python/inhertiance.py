#Super():
# If we want to get base class initializer(__init__) variables, we need to use super() in derived class.

#MRO:

# If a class is inherited from two different classes,
# and two base classes have same common function. If you call that common function in derived class,
# based on MRO rule, based on the order of inhertinace function will call. example

class Base1:
    def fun(self):
        print("Base.fun")

class Base2: #pass
    def fun(self):
        print("Base2.fun")

class Derived(Base1, Base2):
    def fun(self):
        print("Derived.fun")


dobj = Derived()
print(Derived.__mro__)
print(dir(dobj))
print(dir(Derived))
dobj.fun()