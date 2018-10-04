def openOrSenior(data):
    result=[]
    for i in data:
        print i[0]
        if i[0]>=55 and i[1]>7:
            result.append('Senior')
        else:
            result.append('Open')
    return result

def openOrSenior1(data):
    return ['Senior' if  m[0] >= 55 and m[1] > 7 else 'Open' for m in data]
result= openOrSenior1([[45, 12],[55,21],[19, -2],[104, 20]])

print result