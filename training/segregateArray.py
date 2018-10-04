def segregate(arr):
    res = ([x for x in arr if x == 0]) + ([x for x in arr if x == 1])
    return res

# Driver program
if __name__ == "__main__":
    arr = [0, 1, 0, 1, 0, 0, 1, 1, 1, 0]
    res = segregate(arr)
    print(res)
