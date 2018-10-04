
class Context(object):
    """
        How to do base operations on yaml data, like updating and retrieving details
    """
    def __init__(self, ctx=None):
        if issubclass(type(ctx), Context):
            self.__dict__.update(**ctx.__dict__)
        else:
            self._init_context(ctx)

    def _init_context(self, ctx):
        raise NotImplementedError(
            'Initializing context is not implemented')

    def __getitem__(self, item):
        if hasattr(self, str(item)):
            return getattr(self, str(item))
        else:
            return None

    def __setitem__(self, key, value):
        self.__setitem(self, str(key), value)

    def __iter__(self):
        return vars(self).items()

    def __setitem(self, node, key, value):
        if hasattr(node, key):
            self.__update_attr(node, key, value)
        else:
            setattr(node, str(key), value)

    def __update_attr(self, node, key, value):
        if hasattr(value, '__dict__'):
            for _key, _value in vars(value).items():
                self.__setitem(getattr(node, key), _key, _value)
        elif hasattr(value, 'iteritems'):
            for _key, _value in value.items():
                self.__setitem(getattr(node, key), _key, _value)
        elif hasattr(value, '__iter__'):
            for item in value:
                getattr(node, key).append(item)
        else:
            setattr(node, key, value)