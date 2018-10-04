class queue(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        return self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

q = queue()
print(q.isEmpty())
print(q.enqueue(1))
print(q.isEmpty())
print(q.size())
print(q.dequeue())