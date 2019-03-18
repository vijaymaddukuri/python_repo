import re

s = 'the python and the perl scripting'
pattern= '\\bP.+N\\b' #to make none greedy search we will use ?
m= re.search(pattern, s, re.IGNORECASE)

print(m.group())
print(m.start()) #start index
print(m.end())
print(m.span())