import re

a = "vijay.maddukuri@yahoo.com"

match = re.compile(r"""
^([a-z0-9\.-_]+)
@
([a-z0-9\.-]+)
\.
([a-z]{2,6})$
""", re.VERBOSE | re.IGNORECASE)

match1 = re.compile("""
^\w+
([\.-]?\w+)*
@
\w+([\.-]?\w+)*
\.
\w{2,6}$""", re.VERBOSE|re.IGNORECASE)

search = re.search(match1, a)

print(search)
# print(search.groups())
# print(search.group(1))