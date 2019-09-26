class A():
    def __init__(self):
        print("Initializing: class A")

    def sub_method(self, val):
        print('Printing from class A:', val)

class B(A):
    def __init__(self):
        print("Initializing: class B")
        super().__init__()

    def sub_method(self, val):
        print('Printing from class B:', val)
        super().sub_method(val + 1)

class C(B):
    def __init__(self):
        print("Initializing: class C")
        super().__init__()

    def sub_method(self, val):
        print('Printing from class C:', val)
        super().sub_method(val + 1)

c = C()
c.sub_method(1)

"""
So, from the output we can clearly see that the __init()__ function of class C had been called at first, 
then class B and after that class A. 

The same thing happened by calling sub_method() function.

If your program contains multi-level inheritance, then this super() function is beneficial for you.
"""