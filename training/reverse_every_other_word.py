"""
Reverse every other word in a given string, then return the string.
Throw away any leading or trailing whitespace, while ensuring there is exactly one space between each word.
Punctuation marks should be treated as if they are apart of the word
"""

def reverse_alternate(string):
    sList = string.split()
    count=0
    for i in range(len(sList)):
        count += 1
        if count%2==0:
            temp = sList[i]
            sList[i] = temp[::-1]
    return " ".join(sList)

def reverse_alternate1(string):
    return " ".join(y[::-1] if x%2 else y for x,y in enumerate(string.split()))

def reverse_alternate2(s):
  words = s.split()
  words[1::2] = [word[::-1] for word in words[1::2]]
  return ' '.join(words)

print(reverse_alternate('This       si a  test'))