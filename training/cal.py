def calc(expr):
    cal=0
    values=[]
    expr=expr.split(" ")
    operators='+ - * /'
    if expr[-1] in operators:
        for i in expr:
            if i in operators:
                if i=="+":
                    cal=cal+reduce(lambda x, y: x + y, values)


                    values=[]
                elif i=="-":
                    cal =cal + reduce(lambda x, y: x - y, values)
                    values = []
                elif i=="*":
                    cal = cal+reduce(lambda x, y: x * y, values)
                    values = []
                elif i == "/":
                    cal = cal+reduce(lambda x, y: x / y, values)
                    values = []
            else:
                values.append(int(i))

        return cal

    else:
        if '.' in expr[-1]:
            return float(expr[-1])
        elif expr[-1]=="":
            return expr[-1]
        else:
            return int(expr[-1])



a=calc("1 3 4 + 3 - 1")
print a
