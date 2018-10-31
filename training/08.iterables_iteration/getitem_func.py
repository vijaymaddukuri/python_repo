"""
__getitem__(): Alternative iterable protocol works with any object that supports consecutive integer indexing
"""

class AlternativeIterable:
    def __init__(self):
        self.data = [1,2,3]

    def __getitem__(self, index):
        return self.data[index]

for i in AlternativeIterable():
    print(i)
