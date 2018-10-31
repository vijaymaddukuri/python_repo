"""
iterable: An object which implements the __iter__() method

iterator: An object which implements the iterable protocol and which implements the __next__() method.
"""

class ExampleIterator:
    def __init__(self, data):
        self.index = 0
        self.data = data

    def __iter__(self):
        return self

    def __next__(self):
        if self.index>=len(self.data):
            raise StopIteration()

        result = self.data[self.index]
        self.index+=1
        return result

class ExampleIterable:
    def __init__(self):
        self.index = 0
        self.data = [1,2,3]

    def __iter__(self):
        return ExampleIterator(self.data)

for i in ExampleIterable():
    print(i)

