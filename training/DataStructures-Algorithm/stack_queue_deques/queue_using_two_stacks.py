"""
A queue is an abstract data type that maintains the order in which elements were added to it,
allowing the oldest elements to be removed from the front and new elements to be added to the rear.
This is called a First-In-First-Out (FIFO) data structure because the first element added to the queue
(i.e., the one that has been waiting the longest) is always the first one to be removed.

A basic queue has the following operations:

Enqueue: add a new element to the end of the queue.
Dequeue: remove the element from the front of the queue and return it.

1 x: Enqueue element  into the end of the queue.
2: Dequeue the element at the front of the queue.
3: Print the element at the front of the queue.
"""
class queueUsingTwoStacks:
    def __init__(self):
        self.orderedStack = []
        self.reversedStack = []

    def reverseAndPop(self):
        if (not self.reversedStack):
            while (self.orderedStack):
                self.reversedStack.append(self.orderedStack.pop())
        if (self.reversedStack):
            return self.reversedStack.pop()
        return None

    def enqueue(self, data):
        self.orderedStack.append(data)

    def dequeue(self):
        return self.reverseAndPop()

    def frontOfQueue(self):
        front = self.reverseAndPop()
        print(front)
        self.reversedStack.append(front)


q = queueUsingTwoStacks()
cmd = [1, 42, 43]
print((cmd[2:]))
if cmd[0] is "1":
    q.enqueue((cmd[2:]))
elif cmd[0] is "2":
    q.dequeue()
elif cmd[0] is "3":
    q.frontOfQueue()