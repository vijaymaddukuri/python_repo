import abc

class Shape(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass

class Rect(Shape):
    def draw(self):
        return '[ ]'

s = Rect()
print (s.draw())