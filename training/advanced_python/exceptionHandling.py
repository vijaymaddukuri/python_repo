def diviI(num, den):
    if den:
        return num//den
    raise BaseException("Den is zero")

try:
    print(diviI(150,0))
except BaseException as exObj:
    print("Base exception caught", exObj)

print("ENd of the module")

class myExcept:
    def __init__(self, errInfo='myExcept type err'):
        self.info = errInfo

    def __repr__(self):
        return "myExcept.repr" + self.info

    def __str__(self):
        return "myExcept.str" + self.info

def diviI(num, den):
    if den:
        return num//den
    raise myExcept("Den is zero")

try:
    print(diviI(150,0))
except myExcept as exObj:
    print("Base exception caught", exObj)

print("ENd of the module")