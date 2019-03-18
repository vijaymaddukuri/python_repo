import re
pwd='6tIjqWLeRoTNUi\pYs'

#re.search(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s)(?!.*\W).{6,}$', pwd )
if re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{6,}$', pwd):
    a=True
else:
    a=False

print(a)