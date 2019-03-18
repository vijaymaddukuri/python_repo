def isSquare(itemList):
    FinalList=[]
    for value in itemList:
        item = 0
        while item*item < value:
            item=item+1
            if item*item == value:
                newItem=item
            else:
                newItem=value*value
        FinalList.append(newItem)
    return FinalList

itemList=[1,2,3,4,9,10]

newList=isSquare(itemList)
print(newList)

def sqrt(x):
    guess=x
    i=0
    while guess*guess!=x and i < 20:
        guess=(guess+x/guess)/2.0
        i+=1
    return guess
def main():
    try:
        print(sqrt(9))
    except ZeroDivisionError:
        print("Cannot compute for negative number")
    print("Program execution continues")
