import sys

def convert(s):
    ''' COnvert to an integer'''
    try:
        return int(s)
    except (ValueError, TypeError) as e:
        print("Conversion error: {}"\
              .format(str(e)))
        raise ValueError("Cannot convert string to int")

print(convert("hh"))