import re

a="""
I am vijay kumar 1,2,3
vijay,
vijay,
vijay
kumar
M
()(**
"""
c=re.findall("\bVij\b",a)
b=re.findall("[^,]+",a)
b=re.split(',',a,3)
b=re.subn(",","-",a)
#com=re.compile("vijay")
#b=com.findall(a)
#b=re.finditer("\\bkumar\\b",a)
print(b[0][-1])

tup=(0,1)
print(tup[0])