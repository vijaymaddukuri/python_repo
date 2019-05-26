
import sys
def is_represents_int(input_str):
    """
    Checks whether given string is integer or not.
    :param input_str: string.
    :return: boolean.
    """
    try:
        int(input_str)
        return True
    except ValueError:
        return False

def solution(A):
    """
    Calculates the smallest digit number of given number(as a string).
    :param A: Integer.
    :return: smallest possible digit number.
    """
    length=len(str(A))

    if length==1:
        smallest_int = "0"
    else:
        smallest_int = "1" + "0"*(length - 1)
    return int(smallest_int)

print(solution(199))