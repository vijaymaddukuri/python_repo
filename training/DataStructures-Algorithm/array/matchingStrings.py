"""
Sparse Arrays (There is a collection of input strings and a collection of query strings. For each query string,

determine how many times it occurs in the list of input strings.)
"""

def matchingStrings(strings, queries):
    count = []
    for i in queries:
        count.append(str(strings.count(i)))
    return count

count = (matchingStrings(['def', 'de', 'fgh'], ['de', 'lmn', 'fgh']))

for i in count:
    print(i)