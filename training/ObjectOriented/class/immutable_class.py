class immutable(object):
    def __init__(self, immutable_params):
        self.immutable_params = immutable_params

    def __call__(self, new):
        params = self.immutable_params

        def __set_if_unset__(self, name, value):
            if name in self.__dict__:
                raise Exception("Attribute %s has already been set" % name)

            if not name in params:
                raise Exception("Cannot create atribute %s" % name)

            self.__dict__[name] = value

        def __new__(cls, *args, **kws):
            cls.__setattr__ = __set_if_unset__

            return super(cls.__class__, cls).__new__(cls, *args, **kws)

        return __new__

class Point(object):
    @immutable(['x', 'y'])
    def __new__():
        pass

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.x = 3 # Exception: Attribute x has already been set
p.z = 4 # Exception: Cannot create atribute z