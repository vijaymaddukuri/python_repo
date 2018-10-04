# Two strings are anagrams of each other if the letters of one string can be rearranged to form the other string.
# Given a string, find the number of pairs of substrings of the string which are anagrams of each other.
# abba -> [a,a] [ab,ba], [b,b], [abb,bba] - Ans 4
def anagaram(word):
    d = {}
    lst = [word[i:j] for i in range(len(word)+1) for j in range(i, len(word)+1) if i<j ]
    counter = 0
    for item in lst:
        item = ''.join(sorted(item))
        d[item] = d.get(item, 0)+ 1
        if d[item]>1:
            counter += d[item]-1
    return counter

print(anagaram('ifailuhkqq'))

