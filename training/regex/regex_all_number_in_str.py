import re

def getNumbers(str):
    array = re.findall(r'[0-9]+', str)
    return array


# Driver code
str = "adbv345hj43hvb42"
array = getNumbers(str)
print(array)