class Node(object):
    def __init__(self, val):
        self.val = val
        self.next = None

def reverse(head):

    current = head
    prev = None

    while current:
        nextnode = current.next

        current.next = prev

        prev = current
        current = nextnode

a = Node(1)
b = Node(2)
c = Node(3)

a.next = b
b.next = c

print(a.val)
print(a.next.val)
print(b.next.val)

print('\n')
reverse(a)

# print(a.next.val)
print(b.next.val)
print(c.next.val)
print(c.val)