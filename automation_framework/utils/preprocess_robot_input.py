from auc.generic.functions import Functions
from robot.api import logger


def preprocess_kwargs(kwargs):
    """
    Takes all kwargs and if functions are present, calls them
    and replaces with actual values
    :param kwargs:
    :return: Value
    """
    functions = Functions()

    for key, val in kwargs.items():
        if (type(val) is str or type(val) is unicode) and 'function:' in val:
            kwargs[key] = getattr(functions, val.split('function:')[1])()

    return kwargs


def list_2_str(args):
    if isinstance(args, list):
        return ' '.join(str.encode('ascii', 'ignore') for str in args)
    else:
        return args
