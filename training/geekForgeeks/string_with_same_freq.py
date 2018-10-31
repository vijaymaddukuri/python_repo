# Check if a string has all characters with same frequency with one variation allowed

# Input : string str = "abbca"
# Output : Yes
# We can make it valid by removing "c"
#
# Input : string str = "aabbcd"
# Output : No
# We need to remove at least two characters
# to make it valid.
#
# Input : string str = "abbccd"
# Output : No

def isValidString(str):
    dict = {}
    count =0
    for c in str:
        if c in dict.keys():
            dict[c] += 1
        else:
            dict[c] = 1

    values = set(dict.values())
    if len(values) == 1:
        return True

    else:
        for i in dict.keys():
            dict[i]-=1
            temp = list(filter(lambda a: a != 0, dict.values()))
            values = set(temp)
            if len(values) == 1:
                return True
            dict[i]+=1
        return False

print(isValidString('abcdefghhgfedecba'))

