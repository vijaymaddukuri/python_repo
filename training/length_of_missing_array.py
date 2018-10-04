def get_length_of_missing_array(array_of_arrays):
    if array_of_arrays is None:
        return 0
    elif len(array_of_arrays) == 0:
        return 0
    else:
        for i in array_of_arrays:
            if i is None or len(i) == 0:
                return 0

    len_arr = []
    for i in array_of_arrays:
        len_arr.append(len(i))
    len_arr = sorted(len_arr)
    i = 0
    while i < len(len_arr)-1:
        if len_arr[i+1] - len_arr[i] > 1:
            return len_arr[i] + 1
        i += 1

res=get_length_of_missing_array([[1, 2], [4, 5, 1, 1], [1], [5, 6, 7, 8, 9]])
print res