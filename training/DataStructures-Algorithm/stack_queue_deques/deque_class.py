# Deque:
#
# A deque also known as double ended queue, is an ordered collection of items similar to the queue.
#
# It has two ends front and rear and the items remain positioned in the collection.
#
# Unrestricitve nature of adding and removing items makes deque different.
#
# New items can be added at either the front or the rear.
#
# Likewise, existing items can be removed from either end.
#
# This hybrid linear structure provides all the capabilities of stacks and queues in a single data structure.


class Deque(object):

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        return self.items.append(item)

    def addRare(self, item):
        return self.items.insert(0, item)

    def removeFront(self):
        return self.items.pop()

    def removeRare(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

d = Deque()
print(d.addFront('hello'))
print(d.addRare('world'))
print(d.size())
print(d.removeFront() + " " + d.removeRare())
print(d.size())
