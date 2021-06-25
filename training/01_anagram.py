def allAnagram(arr):
    dict = {}
    for word in arr:
        key = ''.join(sorted(word))
        if key in dict:
            dict[key].append(word)
        else:
            dict[key] = []
            dict[key].append(word)
    newLst = ""
    for item in dict.values():
        if len(item) >= 2:
            newLst = newLst + (" ".join(item)) + " "
    print(newLst)

arr = ['cat', 'dog', 'tac', 'god', 'act', 'get']
allAnagram(arr)


