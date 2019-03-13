class doubleLinkedList(object):
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

a = doubleLinkedList(1)
b = doubleLinkedList(2)
c = doubleLinkedList(3)

a.next = b
b.prev = a

b.next = c
c.prev = a

print(a.next.val)
