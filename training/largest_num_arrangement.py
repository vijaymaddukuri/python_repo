def largest_arrangement(numbers):
    for i in range(len(numbers)-1, 0, -1):
        for j in range(i):
            num1 = str(numbers[j])
            num2 = str(numbers[j+1])
            if int(num1[0]) < int(num2[0]):
                temp = numbers[j]
                numbers[j]=numbers[j+1]
                numbers[j+1]=temp
            elif int(num1[0]) == int(num2[0]):
                ab = num1 + num2
                ba = num2 + num1
                if int(ab) < int(ba):
                    temp = numbers[j+1]
                    numbers[j+1] = numbers[j]
                    numbers[j] = temp
    return int("".join([str(i) for i in numbers]))

print(largest_arrangement([7, 78, 79, 72, 709, 7, 94]))