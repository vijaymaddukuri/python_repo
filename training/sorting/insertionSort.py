'''
Start the loop from 1 pos
If the pos > 0 and value in prev pos  > value in current pos- Swap the values and swap the index
'''
def insertionSort(lst):
    for index in range(1,len(lst)):
        currentValue = lst[index]
        pos=index
        while pos>0 and lst[pos-1]>currentValue:
            lst[pos]=lst[pos-1]
            pos=pos-1
        lst[pos]=currentValue
alist = [54,26,93,17,77,31,44,55,20]
insertionSort(alist)
print(alist)



