"""
You’re given the pointer to the head node of a linked list and a specific position.
Counting backwards from the tail node of the linked list, get the value of the node at the given position.
A position of 0 corresponds to the tail, 1 corresponds to the node before the tail and so on.
"""

class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_node(self, node_data):
        node = SinglyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node


        self.tail = node

def print_singly_linked_list(node, sep, fptr):
    while node:
        fptr.write(str(node.data))

        node = node.next

        if node:
            fptr.write(sep)

def getNode(head, position):
  trailingNode = head
  len = 0

  while (head):
    if (len > position):
      trailingNode = trailingNode.next

    len += 1
    head = head.next

  return trailingNode.data