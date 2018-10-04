from fileinput import input, filename, filelineno

for line in input([r'C:\Users\madduv\Desktop\resourceOperations.txt']):
    print('{}:{}:{}'.format(filename(), filelineno(), line))
