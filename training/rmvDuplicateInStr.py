#Remove duplicate characters in a given string keeping only the first occurrences.
# For example, if the input is tree traversal the output will be tre avsl

def rmvDuplicate(str):
    newStr=''
    for chr in str:
        if chr not in newStr:
            newStr = newStr+chr
    return newStr

print(rmvDuplicate("tree traversal"))