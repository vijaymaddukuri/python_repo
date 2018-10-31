"""
static method - learn
class method - learn


"""

class cA:
    @classmethod
    def classMethod(cls, arg=10):
        cls.m_i = arg
cA.classMethod(112)

print("cA.m_i =", cA.m_i)
