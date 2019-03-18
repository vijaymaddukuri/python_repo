def index(name,val):
    last=name.rfind(val[-1])
    start=0
    tup=[]
    for i in range(last+1):
        start=name.index(val[0],start)

        end=name.index(val[-1],start+1)
        tup.append((start, end))
        if end==last:
            break
        else:
            start+=1
            end+=1
    print(tup)

def findIndex(name,val):
    import re
    compilerStart=re.compile(val[0])
    compilerEnd = re.compile(val[-1])
    for m in compilerStart.finditer(name):
        print(m.start(), m.group())
    for n in compilerEnd.finditer(name):
        print(n.start(), n.group())


a=findIndex('aaabcaab','ab')