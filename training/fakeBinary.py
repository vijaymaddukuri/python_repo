def fake_bin(x):
    temp=[]
    for i in str(x):
        print(int(i))
        if int(i)<5:
            value=0
            temp.append(value)
        elif int(i)>=5:
            value=1
            temp.append(value)
    return ''.join(str(e) for e in temp)

def fake_bin1(x):
    result = ""
    for num in str(x):
        if int(num) < 5:
            result = result + "0"
        else:
            result = result + "1"
    return result

def fake_bin3(x):
    return ''.join('0' if c < '5' else '1' for c in x)

bin=fake_bin1("5432345718192")
print(bin)

