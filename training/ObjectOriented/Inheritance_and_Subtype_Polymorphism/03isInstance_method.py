"""
isinstance(): Determines if an object is of a specified type. Used for run time type checking
"""
print(isinstance(3, int))
print(isinstance('hello', str))
print(isinstance(4.567, bytes))
x=[]
print(isinstance(x, (float, int, list)))

class SimpleList:
    def __init__(self, items):
        self._items= items

    def add(self, item):
        self._items.append(item)

    def __getitem__(self, index):
        return self._items[index]

    def sort(self):
        self._items.sort()

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return "SimpleList({!r})".format(self._items)

class IntList(SimpleList):
    def __init__(self, _items=()):
        for x in _items: self._validate(x)
        super().__init__(_items)

    @staticmethod
    def _validate(x):
        if not isinstance(x, int):
            raise TypeError('Intlist only supports integer values')

    def add(self, item):
        self._validate(item)
        super().add(item)

    def __repr__(self):
        return "Intlst {}".format(list(self))

il = IntList([1,2,3,'5'])
il = IntList([1,2,3])
il.add('vijay')