def basic_op(operation,item1,item2):
    if operation == '+':
        return item1+item2
    elif operation == '-':
        return item1-item2
    elif operation == '/':
        return  item1/item2
    elif operation == '*':
        return item1*item2
    elif operation == '%':
        return item1%item2
    else:
        return "Invalid operater"

def basic_op2(operator, value1, value2):
    ops = {'+': lambda a, b: a + b,
           '-': lambda a, b: a - b,
           '*': lambda a, b: a * b,
           '/': lambda a, b: a / b}
    return ops[operator](value1, value2)
def basic_op3(o, a, b):
    return {'+':a+b,'-':a-b,'*':a*b,'/':a/b}.get(o)

value = basic_op3('+', 4, 7)

print(value)

