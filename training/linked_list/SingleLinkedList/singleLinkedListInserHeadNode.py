class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insertHead(self, newNode):
        if self.head is None:
            self.head = newNode
            return
        tempNode = self.head
        self.head = newNode
        self.head.next = tempNode
        del tempNode

    def insertEnd(self, newNode):
        if self.head is None:
            self.head = newNode
        else:
            lastNode = self.head
            while True:
                if lastNode.next is None:
                    break
                lastNode = lastNode.Next
            lastNode.next = newNode

    def printLinkedList(self):
        if self.head is None:
            print("List is empty")
            return
        currentNode = self.head
        while True:
            if currentNode is None:
                break
            print(currentNode.data)
            currentNode = currentNode.next

def insertNodeAtHead(llist, data):
    if llist is None:
        return SinglyLinkedListNode(data)
    tempNode = llist
    head = SinglyLinkedListNode(data)
    head.next = tempNode
    del tempNode
    return head

node1 = Node('vijay')
node2 = Node('vicky')
node3 = Node("Maddukuri")
linkedList = LinkedList()
linkedList.insertEnd(node1)
linkedList.insertEnd(node2)
linkedList.insertHead(node3)
linkedList.printLinkedList()
