class RangeError(Exception):
    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.args)

def check_range(value):
    if not 0.3 <= value <= 0.7:
        raise RangeError('value not in the range: {}'.format(value))
    return True

if __name__ == '__main__':
    check_range(.2)