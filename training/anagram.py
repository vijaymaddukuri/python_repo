def isAnagaram(arr):
    anagram_list=[]
    for i in range(len(arr)):
        sort_arr1 = sorted(arr[i])
        for j in range(len(arr)):
            if arr[i]!=arr[j]:
                sort_arr2=sorted(arr[j])
                if sort_arr1 == sort_arr2:
                    anagram_list.append(arr[i])
    return anagram_list

print(isAnagaram(["car", "tree", "boy", "girl", "arc"]))


