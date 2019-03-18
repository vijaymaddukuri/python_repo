def median(s,x):
    if(s == 'r' and len(list) == 0):
        print("Wrong!")
    elif(s == 'r'):
        list.remove(x)
        print(printMedian(list))
    elif(s == 'a'):
        list.append(x)
        list.sort()
        print(printMedian(list))

def printMedian(itemList):
    length = len(itemList)
    if length == 0:
        return "Wrong!"
    if int(length % 2) == 1:
        return (itemList[(int((length + 1) / 2)) - 1])
    else:
        return float(sum(itemList[int((length / 2)) - 1:int((length / 2)) + 1])) / 2.0

N = int(input())
list = []
for i in range(0, N):
    tmp = input().strip().split(' ')
    s = tmp[0]
    element = int(tmp[1])
    median(s,element)