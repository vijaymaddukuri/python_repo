import re
fileLocation=r'D:\new\vijay.txt'
file=open(fileLocation,'r+')
read=file.read().split()
line= ' '.join(read)

print(read)
unique=set(read)

print(unique)
dict={}
for temp in unique:
    count = re.findall('\\b'+temp+'\\b',' '.join(read))
    #count = line.count(temp)
    print(count)
    dict[temp]=len(count)
print(dict)





