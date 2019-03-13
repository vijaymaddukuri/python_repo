def argument_logger(func):
    """Decorator"""
    def logger_handler(*args, **kwargs):
        """Decorator Handler"""
        return_value=func(*args)
        print("args: {} returns: {}".format(args, return_value))
        return return_value
    return logger_handler

class Trace:
    def __init__(self):
        self.enable=True
    def __call__(self, func):
        def wrap(*args, **kwargs):
            if self.enable:
                print('calling {}'.format(func))
            return func(*args, **kwargs)
        return wrap

tracer = Trace()

class Power:

    @tracer
    @argument_logger
    def power(self, x, y):
        return x ** y

obj = Power()
obj.power(2, 3)