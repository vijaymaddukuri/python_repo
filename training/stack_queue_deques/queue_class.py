# Queue:
#
# A queue is an ordered collection of items where the addition of new items happens at one end, called the rear.
#
# And the removal of existing items occurs at the other end, commonly called the front.
#
# As an element enters into the queue, it starts at the rear and makes its way toward the front,
# waiting until that time
# when it is the next element to be removed.
#
# Most recently added item in the queue must wait at the end of the collection (FIFO) or (FCFS)
#
# Example: Movie ticket queue or grocery store queue.
#
# Enqueue: Adding item to queue
# Dequeue: Removing front item from the queue


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