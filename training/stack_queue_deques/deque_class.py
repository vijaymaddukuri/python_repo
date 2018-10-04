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
