import re

search = re.compile('^[aeiouAEIOU][a-zA-Z0-9]*')

name = "vijay"
name2 = "apple"

print(re.search(search, name))

print(re.search(search, name2))