def repeatCount(sentance):
    words=sentance.split(" ")
    print words
    dict={}
    for n in words:
        keys=dict.keys()
        print n
        if n in keys:
            dict[n]+=1
        else:
            dict[n]=1
    return dict

sentance='I am vijay I vijay'
count=repeatCount(sentance)
print count


# Complete the degreeOfArray function below.
def degreeOfArray(arr):
    map_dictionary = {}
    for element in arr:
        map_dictionary[element] = map_dictionary.get(element, 0) + 1

    degree = max(map_dictionary.values())
    # return degree
    sub_list = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            sub = arr[i:j]
            for element in arr:
                if sub.count(element) == degree:
                    sub_list.append(sub)

    return min([len(a) for a in sub_list])


# Complete the degreeOfArray function below.
def degreeOfArray(arr):
    map_dictionary = {}
    for element in arr:
        map_dictionary[element] = map_dictionary.get(element, 0) + 1

    degree = max(map_dictionary.values())
    # return degree
    sub_list = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            sub = arr[i:j]
            for element in arr:
                if sub.count(element) == degree:
                    sub_list.append(sub)

    return min([len(a) for a in sub_list])




