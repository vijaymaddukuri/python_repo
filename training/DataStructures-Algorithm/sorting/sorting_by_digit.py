

def order(sentence):
    import re
    sentence=sentence.split(" ")
    temp=[]
    for i in range(len(sentence)-1,0,-1):
        for j in range(i):
            obj=re.search('\d+',sentence[j])
            obj1 = re.search('\d+', sentence[j+1])
            if obj.group(0)>obj1.group(0):
                temp=sentence[j]
                sentence[j]=sentence[j+1]
                sentence[j+1]=temp
    return " ".join(sentence)

newSen=order('is21 Thi1s2 T4est 2a')
print(newSen)
