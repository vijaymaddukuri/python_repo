class queue(object):
    def __int__(self):
        self.item=[]

    def isQueueEmplty(self):
        return self.item==[]

    def enqueue(self,item):
        self.item.insert(0,item)

    def dequeue(self,item):
        self.item.pop()

    def size(self,item):
        return len(self.item)

q=queue()
q.enqueue(4)
print(q.size())