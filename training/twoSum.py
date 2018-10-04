def two_sum(numbers, target):
    for i in range(len(numbers)):
        for j in range(1, len(numbers)):
            if numbers[i]+numbers[j]==target:
                return i,j
    return None

def two_sum1(numbers, target):
    return [[i, numbers.index(target - numbers[i])] for i in range(len(numbers)) if target - numbers[i] in numbers].pop()
print(two_sum([2,3,3], 4))

