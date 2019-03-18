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

# custom comparator to sort according
# to the ab, ba as mentioned in description
def comparator(a, b):
    ab = str(a) + str(b)
    ba = str(b) + str(a)
    return ((int(ba) > int(ab)) - (int(ba) < int(ab)))

def myCompare(mycmp):

    # Convert a cmp= function into a key= function
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
            print(self.obj)


        def __lt__(self, other):
            print('**')
            print(other.obj)
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K
    # driver code

if __name__ == "__main__":
    a = [7, 78, 79, 72, 709, 7, 94 ]
    sorted_array = sorted(a, key=myCompare(comparator))
    number = "".join([str(i) for i in sorted_array])
    print(number)

print(largest_arrangement([7, 78, 79, 72, 709, 7, 94]))