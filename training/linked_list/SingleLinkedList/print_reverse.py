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

def print_singly_linked_list(node, sep):
    while node:
        print(node.data, end='')

        node = node.next

        if node:
            print(sep, end='')

def reversePrint(head):
    if head:
        reversePrint(head.next)
        print(head.data)
def ReversePrint(head):
    if head is None:
        return None
    else:
        stack = []
        while head:
            stack.append(head.data)
            head = head.next
        while stack:
            print(stack.pop())

if __name__ == '__main__':
    tests = [1,2,3,4]

    for tests_itr in tests:
        llist_count = tests_itr

        llist = SinglyLinkedList()

        for _ in range(llist_count):
            llist_item = int(input())
            llist.insert_node(llist_item)

        reversePrint(llist.head)
