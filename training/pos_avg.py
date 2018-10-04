# "466960, 069060, 494940, 060069, 060090, 640009, 496464, 606900, 004000, 944096", 26.6666666667)
# "444996, 699990, 666690, 096904, 600644, 640646, 606469, 409694, 666094, 606490", 29.2592592593)

def compare(a,b):
    count=0
    if a==b:
        return 0
    for i in range(len(a)-1):
        if a[i]==b[i]:
            count+=1
    return count

def pos_average(s):
    count=0
    s=s.split(", ")
    print(s)
    for pos, item in enumerate(s):
        for item1  in s[pos:]:
            if item!=item1:
                temp=compare(item, item1)
                print(item, item1, temp)
                count=temp+count
    total_count=count
    print(total_count)
    eLen=len(s)*(len(s)-1)/2
    print(eLen)
    avg=(total_count/eLen)*100
    return avg

average = pos_average("466960, 069060, 494940, 060069, 060090, 640009, 496464, 606900, 004000, 944096")
print(average)

