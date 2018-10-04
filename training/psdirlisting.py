from os import listdir
from os.path import isfile, join, getsize, getmtime
from time import ctime
from pprint import pprint as pp

class DirectoryListing:
    def __init__(self, *args):
        self.directories = args
        self.container = {}
        self.__read_directory()

    def __read_directory(self):
        for dir_name in self.directories:

            for file_name in listdir(dir_name):
                abs_path = join(dir_name, file_name)

                if isfile(abs_path):
                    size = getsize(abs_path)
                    mtime = ctime(getmtime(abs_path))
                    self.container.setdefault(dir_name, {})[file_name]= [size, mtime]

if __name__ == '__main__':
   d1 = DirectoryListing(r'c:\users\madduv\Desktop')
   pp(d1.container)

