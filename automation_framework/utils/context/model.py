class YAMLData(object):
    def __init__(self, **kwargs):
        """
        Description: Read the yaml time and generate dictionary
        :returns: input dictionary
        """
        for key, value in kwargs.items():
            if hasattr(value, 'iteritems'):
                self.__dict__.__setitem__(key, YAMLData(**value))
            elif hasattr(value, '__iter__'):
                self.__dict__.__setitem__(key, [])

                for item in value:
                    if hasattr(item, 'iteritems'):
                        self.__dict__.__getitem__(key).append(YAMLData(**item))
                    else:
                        self.__dict__.__getitem__(key).append(item)
            else:
                self.__dict__.__setitem__(key, value)