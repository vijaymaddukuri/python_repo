A = "25525511135"
B = "22221"

def validateIP(ip):
    splitIP=ip.split('.')
    for octate in splitIP:
        if len(octate)>3 or int(octate)<0 or int(octate)>255:
            return False
        if len(octate)>1 and int(octate)==0:
            return False
        if len(octate)>1 and int(octate)!=0 and int(octate[0])==0:
            return False
    return True

sz=len(B)
temp=B
IPlist=[]
for i in range(1, sz -2):
    for j in range(i+1, sz-1):
        for k in range(j+1,sz):
            temp=temp[:k]+'.'+temp[k:]
            temp=temp[:j]+'.'+temp[j:]
            temp=temp[:i]+'.'+temp[i:]
            if temp != '':
                if validateIP(temp):
                    IPlist.append(temp)
            temp=A
print(IPlist)


