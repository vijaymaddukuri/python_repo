def fraction(arr):
    splitFnum=arr[0]
    for num in range(1,len(arr)):
        splitNum=str(arr[num]).split("/")
        splitFnum = str(splitFnum).split("/")
        if splitFnum[1]==splitNum[1]:
            upper=str(int(splitNum[0])+int(splitFnum[0]))
            lower=splitNum[1]
            splitFnum = str(upper) + "/" + lower
        elif splitFnum[1]>splitNum[1]:
            diff=int(splitFnum[1])/int(splitNum[1])
            upper=int(splitNum[0])*diff
            lower=splitFnum[1]
            splitFnum = str(upper) + "/" + lower
        else:

            diff=int(splitNum[1])/int(splitFnum[1])
            upper=int(splitFnum[0])*diff+int(splitNum[0])
            lower=splitNum[1]
            splitFnum= str(upper) + "/" + lower
    temp  = str(splitFnum).split("/")
    mod = int(temp[0])%int(temp[1])
    print mod
    div = int(temp[0])/int(temp[1])
    if mod==0:
        return str(div)
    else:
        return splitFnum

print fraction(['-2/3', '5/3', '-4/6'])


