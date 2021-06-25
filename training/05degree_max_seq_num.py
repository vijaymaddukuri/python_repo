def degree(arr):
    dict={}
    for i in arr:
        dict[i] = dict.get(i, 0) + 1
    deg = max(dict.values())

    for i in range(0,len(arr)-deg):
        for j in range(0, len(arr)-deg):
            sub = arr[j:j+i+deg]
            for k in set(sub):
                # print sub
                if sub.count(k) == deg:
                    return len(sub)

def degree2(arr):
    dict = {}
    for index, element in enumerate(arr):
        if element in dict:
            dict[element][0] += 1
            dict[element][2] = index
        else:
            dict[element]= [1, index, index]

    maxDeg = max([degr for degr, _ ,_ in dict.values()])
    return min([endindex-startindex+1 for degr, startindex, endindex in dict.values() if degr==maxDeg])


lst=[1, 1, 2, 1, 2, 2]
print(degree2(lst))
print(degree(lst))