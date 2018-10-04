def balance_check(arr):
    open_bracs='([{'
    matches = [('(',')'), ('[',']'), ('{','}')]
    stack = []
    for item in arr:
        if item in open_bracs:
            stack.append(item)
        else:
            if len(item)==0:
                return False
            last_open = stack.pop()
            if (last_open, item) not in matches:
                return False
    return len(stack) == 0

value=balance_check('[{{{(())}}}]((()))')
print(value)
value=balance_check('[{]{')
print(value)


