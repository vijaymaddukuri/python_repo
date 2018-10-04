def countTriple(arr, r):
    dict={}
    dict2={}
    count=0
    for i in arr:
        dict[i]=dict.get(i, 0) +1
    for i in arr:
        dict[i]-=1
        if dict[i]%r==0:
            print dict[i]/r
            print dict2
            if dict[i]/r in dict2:
                count+=dict2[dict[i]/r]*dict[dict[i]*r]
        dict2[i] = dict2.get(i, 0) + 1
    print count



countTriple([1,2, 4,16,24,1,8,32],4)