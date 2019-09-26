"""
Input : BruceWayneIsBatman
Output : bruce wayne is batman

Input :  GeeksForGeeks
Output :  geeks for geeks
"""

word = 'BruceWayneIsBatman'

import re

a = re.sub('([A-Z])', r' \1', word)
b = re.sub('^\s*', '', a)
print(b.lower())

