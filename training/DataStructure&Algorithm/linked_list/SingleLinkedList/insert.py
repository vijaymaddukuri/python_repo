class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Solution:
    def display(self,head):
        current = head
        while current:
            print(current.data,end=' ')
            current = current.next

    def insert(self,head,data):
        if not head:
            return Node(data)
        head.next = self.insert(head.next, data)
        return head


mylist= Solution()
T=[1,2,3,4,5]
head=None
for i in T:
    data=i
    head=mylist.insert(head,data)
mylist.display(head)