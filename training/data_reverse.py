"""
A stream of data is received and needs to be reversed.
Each segment is 8 bits long, meaning the order of these segments need to be reversed, for example:

11111111  00000000  00001111  10101010
  byte1     byte2     byte3     byte4
should become:

10101010  00001111  00000000  11111111
  byte4     byte3     byte2     byte1
"""

def data_reverse(data):
    l = len(data)
    s = 0
    lst = []
    for i in range(0,l+1,8):
        if i !=0:
            temp = data[s:i]
            lst.append(temp)
        s=i
    finalList = []
    for item in range(len(lst)):
        temp = lst.pop(-1)
        finalList.extend(temp)
    return finalList


def data_reverse1(data):
    res = []

    for i in range(len(data) - 8, -1, -8):
        print(i)
        res.extend(data[i:i + 8])

    return res

data = [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,1,0,1,0]
print(data_reverse1(data))