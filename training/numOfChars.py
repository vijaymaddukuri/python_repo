def numOfChars(name):
    dict={}
    for n in name:
        keys=dict.keys()
        if n in keys:
            dict[n]+=1
        else:
            dict[n]=1
    return dict

print(numOfChars('Vijay'))