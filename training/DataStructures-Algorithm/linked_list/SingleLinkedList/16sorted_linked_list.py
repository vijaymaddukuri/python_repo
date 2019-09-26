class Node:
    def __init__(self, data, _next=None):
        self.data = data
        self.next = _next

def main():
    nodes = []
    num = int(input("Enter number: "))
    while num != -1:
        nodes.append(Node(num))
        num = int(input("Enter number: "))

    # If list is empty then just end function
    if len(nodes) == 0:
        return

    # Let python do the sorting
    nodes = sorted(nodes, key=lambda node: node.data)

    # Link the nodes together and print them while you're at it
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
        print(nodes[i].data)
    # We need to print the last node
    print(nodes[-1].data)

main()


# class Node:
#     def __init__(self):
#       self.data = None
#       self.next = None
#
# class LinkedList:
#     def __init__(self):
#       self.head = None
#
#     def addNode(self, data):
#       curr = self.head
#       if curr is None:
#         n = Node()
#         n.data = data
#         self.head = n
#         return
#
#       if curr.data > data:
#         n = Node()
#         n.data = data
#         n.next = curr
#         self.head = n
#         return
#
#       while curr.next is not None:
#         if curr.next.data > data:
#           break
#         curr = curr.next
#       n = Node()
#       n.data = data
#       n.next = curr.next
#       curr.next = n
#       return
#
#     def __str__(self):
#       data = []
#       curr = self.head
#       while curr is not None:
#         data.append(curr.data)
#         curr = curr.next
#       return "[%s]" %(', '.join(str(i) for i in data))
#
#     def __repr__(self):
#       return self.__str__()
#
# def main():
#     ll = LinkedList()
#     num = int(input("Enter a number: "))
#     while num != -1:
#       ll.addNode(num)
#       num = int(input("Enter a number: "))
#     c = ll.head
#     while c is not None:
#       print(c.data)
#       c = c.next

# main()