import re
from fileinput import input, filename, filelineno

class GrepMe:
    def __init__(self, pattern, *args):
        self.file_names = args
        self.pattern=pattern
        self.__find_match()

    def __find_match(self):
        for line in input(self.file_names, inplace=True, backup='.bak'):
            if re.search(self.pattern, line, re.I):
                line=re.sub(self.pattern,'.',line)
                print('{}:{}:{}'.format(filename(), filelineno(), line))

if __name__ == '__main__':
    GrepMe(':', r'C:\Users\madduv\Desktop\tmp.json')