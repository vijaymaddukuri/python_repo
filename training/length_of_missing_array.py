def get_length_of_missing_array(arr):
    if arr is None:
        return 0
    elif len(arr) == 0:
        return 0
    lst = sorted(list(map(len, arr)))
    first=lst[0]
    for i in lst[1:]:
        if i == 0:
            return 0
        if i-first>1:
            return first+1
        first=i
    return 0


print(get_length_of_missing_array([[0]]))
print(get_length_of_missing_array([[1, 2], [4, 5, 1, 1], [1], [5, 6, 7, 8, 9]]))
print(get_length_of_missing_array([[]]))