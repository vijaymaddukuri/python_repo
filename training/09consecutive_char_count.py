"""
Consecutive repeated char count
Input:AAABBCAA
Output: A3B2CA2


"""
def string_count(arr):
    first = arr[0]
    count = 1
    new_str = ''
    for item in arr[1:]:
        if first == item:
            count += 1
        else:
            if count > 1:
                new_str += first + str(count)
            else:
                new_str += first
            count = 1
            first = item
    if count > 1:
        new_str += first + str(count)
    else:
        new_str += first

    return new_str


print(string_count('AAABB'))