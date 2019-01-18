import re
div_4 = '^\d+$'

def re_test(input_str):
    match = re.match(div_4, input_str)

    if match:
        if (int(input_str))%4==0:
            return True
        else:
            return False
    else:
        return False

print(re_test('1024'))