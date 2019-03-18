import re
s='vijay,kumar:m;y'

items = re.split(',|;|:',s)
print(items)

