def find_outlier(integers):
    evenList = []
    oddList = []
    for i in integers:
        if i % 2 == 0:
            evenList.append(i)
        else:
            oddList.append(i)
    if len(evenList) < len(oddList):
        result = evenList[0]
    else:
        result = oddList[0]

    return result

result = find_outlier([2,6,8,10,3])

print(result)