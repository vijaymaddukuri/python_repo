import re
def minimumNumber(n, password):
    password = str(password)
    count = 0
    lowerObj = re.findall('[a-z]', password)
    if lowerObj:
        count+=1
    upperObj = re.findall('[A-Z]', password)
    if upperObj:
        count+=1
    digObj = re.findall('[0-9]', password)
    if digObj:
        count+=1
    specialObj = re.findall('[^A-Za-z0-9]', password)
    if specialObj:
        count+=1
    if count == 4 and n >= 6:
        return 0
    elif count < 4 and n < 6:
        covered = 4-count #3
        l = 6 - n # 2
        if covered > l:
            return covered
        else:
            return l
    elif count < 4 and n >= 6:
        return 4-count
    elif count == 4 and n < 6:
        return 6-n

print(minimumNumber(4, '4700'))
print(minimumNumber(3, 'Ab1'))
print(minimumNumber(11, '#HackerRank'))

numbers = "0123456789"
lower_case = "abcdefghijklmnopqrstuvwxyz"
upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
special_characters = "!@#$%^&*()-+"


def minimumNumber(n, password):
    add = 0
    if all(n not in password for n in numbers):
        add += 1

    if all(l not in password for l in lower_case):
        add += 1

    if all(u not in password for u in upper_case):
        add += 1
    if all(s not in password for s in special_characters):
        add += 1

    return add + max(0, 6 - len(password) - add)