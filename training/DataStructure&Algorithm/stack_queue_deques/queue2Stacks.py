class Queue2Stacks(object):
    def __init__(self):
        self.instack = []
        self.outstack = []

    def enqueue(self, element):
        self.instack.append(element)

    def dequeue(self):
        if not self.outstack:
            while self.instack:
                self.outstack.append(self.instack.pop())
        return self.outstack.pop()

q = Queue2Stacks()
q.enqueue(1)
q.enqueue(2)
print(q.dequeue())



