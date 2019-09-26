"""
super(): Returns a proxy object which routes method calls

Bound proxy: Bound to a specific class or instance.

unbound proxy: Not bound to a class or instance

There are two types of bound proxies:

Instance bound and class bound

Class bound proxy:

Super(base-class, derived class)

 - Python finds the MRO for derived class.
 - Then finds base-class in that MRO
 - It takes every thing after base class in the MRO  and finds the first class in that
 sequence with a matching method name.
"""

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

class SortedList(SimpleList):
    def __init__(self, items=()):
        super().__init__(items)
        self.sort()

    def add(self, item):
        super().add(item)
        self.sort()

    def __repr__(self):
        return "SortedList({!r})".format(list(self))


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


class SortedIntlist(IntList, SortedList):
    def __repr__(self):
        return 'SortedIntList {}'.format(self)


print(super(SortedList, SortedIntlist).add)

"""Proxy bounds to the class not the instance."""

print(super(SortedList, SortedIntlist).add(4))

"""If we proxy to class method or static method, we can invoke directly"""

print(super(SortedIntlist, SortedIntlist)._validate(5))
print(super(SortedIntlist, SortedIntlist)._validate('5'))

"""If the second class is not the subclass of first, python with throw exception"""

print(super(int, IntList))
