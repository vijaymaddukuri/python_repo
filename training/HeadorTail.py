from io import FileIO

class CustomFileIO(FileIO):

    def __rlshift__(self, other):
        return CustomFileIO(self, '<<')
    pass

if __name__ == '__main__':
    fp = CustomFileIO(r'C:\Users\madduv\Desktop\tmp.json')
    print(fp << 5) # last lines