"""
https://www.toptal.com/python/python-design-patterns
"""

class Sublime:
    isinstance_bucket = dict()
    def __init__(self, param):
        if not self.__dict__:
            self.__dict__= Sublime.isinstance_bucket
        self.param= param

    def __str__(self):
        return "id: {} param : {}".format(id(self), self.param)

if __name__ == '__main__':
    o1=Sublime('vijay')
    o2 = Sublime('kumar')
    print(o1)
    print(o2)

